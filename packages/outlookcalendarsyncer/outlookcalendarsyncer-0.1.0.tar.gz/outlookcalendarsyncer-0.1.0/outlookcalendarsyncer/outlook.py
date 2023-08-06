import datetime as dt
import json
import logging
import os.path
from dataclasses import dataclass
from logging import Logger
from typing import List, Optional

from O365 import Account, FileSystemTokenBackend
from O365.calendar import Schedule, EventShowAs
from O365.utils import Query

from outlookcalendarsyncer.configuration import AccountConfiguration

logger: Logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CalendarEvent:
    id: str
    subject: str
    show_as: EventShowAs
    start: dt.datetime
    end: dt.datetime
    is_all_day: bool
    synthetic_hash: Optional[str]


class CalendarChangeEvent:
    pass


@dataclass(frozen=True)
class NewEventChangeEvent(CalendarChangeEvent):
    id: str
    subject: str
    show_as: EventShowAs
    start: dt.datetime
    end: dt.datetime


@dataclass(frozen=True)
class ModifiedEventChangeEvent(CalendarChangeEvent):
    target_event_id: str
    new_subject: str
    new_show_as: EventShowAs
    new_start: dt.datetime
    new_end: dt.datetime


@dataclass(frozen=True)
class DeletedEventChangeEvent(CalendarChangeEvent):
    target_event_id: str


class OfficeAccount:
    def __init__(
        self,
        name: str,
        configuration: AccountConfiguration,
        configuration_base_directory: str,
    ):
        self.__configuration = configuration
        self.__account = Account(
            credentials=(
                self.__configuration.client_id,
                self.__configuration.client_secret,
            ),
            token_backend=FileSystemTokenBackend(
                os.path.join(configuration_base_directory, name)
            ),
            tenant_id=self.__configuration.tenant_id,
        )

        if not self.__account.is_authenticated:
            logger.info(f"[account '{name}'] Not authenticated")
            if self.__account.authenticate(
                scopes=["basic", "calendar_all"],
                redirect_uri=self.__configuration.redirect_uri,
            ):
                logger.info(f"[account '{name}'] Authenticated")
            else:
                logger.info(f"[account '{name}'] Couldn't authenticate for account")
                raise RuntimeError(f"Couldn't authenticate for account '{name}'")

        logger.debug(f"[account '{name}'] Scopes: {self.__account.connection.scopes}")
        self.__account_schedule: Schedule = self.__account.schedule()
        logger.debug(f"[account '{name}'] Schedule: {self.__account_schedule}")
        self.__calendar = self.__account_schedule.get_default_calendar()
        logger.debug(f"[account '{name}'] Default calendar: {self.__calendar}")

    @property
    def configuration(self):
        return self.__configuration

    def list_calendar_events(
        self, weeks_from_now: int, include_recurring=True
    ) -> List[CalendarEvent]:
        def __create_time_query() -> Query:
            current_day = dt.datetime.date(dt.datetime.now())
            end_day = current_day + dt.timedelta(weeks=weeks_from_now)

            logger.debug(f"Start time for query: {current_day}")
            logger.debug(f"End time for query: {end_day}")

            return (
                self.__calendar.new_query("start")
                .greater_equal(current_day)
                .chain("and")
                .on_attribute("end")
                .less_equal(end_day)
            )

        def extract_hash(raw_event):
            try:
                event_content = json.loads(raw_event.get_body_text())
                return event_content["hash"]
            except:
                return None

        raw_events = list(
            self.__calendar.get_events(
                query=__create_time_query(),
                batch=256,
                order_by="start/dateTime asc",
                include_recurring=include_recurring,
            )
        )

        calendar_events = []

        for event in raw_events:
            event.body_type = event.body_type.upper()

            synthetic_hash = extract_hash(event)

            calendar_events.append(
                CalendarEvent(
                    id=event.object_id,
                    subject=event.subject,
                    show_as=event.show_as,
                    start=event.start,
                    end=event.end,
                    is_all_day=event.is_all_day,
                    synthetic_hash=synthetic_hash,
                )
            )

        return calendar_events

    def save_calendar_events(self, events: List[CalendarChangeEvent], prefix: str):
        for event in events:
            if isinstance(event, NewEventChangeEvent):
                logger.info(
                    f"Going to create following new event:"
                    f" {{'subject': '{event.subject}', 'start': '{event.start}', 'end': '{event.end}'}}"
                )

                new_event = self.__calendar.new_event()
                new_event.subject = f"{prefix} {event.subject}"
                new_event.start = event.start
                new_event.end = event.end
                new_event.show_as = event.show_as
                new_event.body = json.dumps({"hash": event.id})

                if new_event.save():
                    logger.info(
                        f"Event has been created successfully. It's id is '{new_event.object_id}'"
                    )
                else:
                    logger.error(f"Could not create new event")

            elif isinstance(event, ModifiedEventChangeEvent):
                logger.info(
                    f"Going to change event with id '{event.target_event_id[:10]}...' with following properties:"
                    f" {{'subject': '{event.new_subject}', 'start': '{event.new_start}', 'end': '{event.new_end}'}}"
                )

                target_event = self.__calendar.get_event(event.target_event_id)
                target_event.subject = f"{prefix} {event.new_subject}"
                target_event.start = event.new_start
                target_event.end = event.new_end
                target_event.show_as = event.new_show_as

                if target_event.save():
                    logger.info(
                        f"Event with id '{target_event.object_id[:10]}...' has been changed successfully"
                    )
                else:
                    logger.error(
                        f"Could not change event with id '{target_event.object_id[:10]}...'"
                    )

            elif isinstance(event, DeletedEventChangeEvent):
                logger.info(
                    f"Going to delete event with id '{event.target_event_id[:10]}...'"
                )
                outlook_event = self.__calendar.get_event(event.target_event_id)
                if outlook_event.delete():
                    logger.info(
                        f"Event with id '{event.target_event_id[:10]}...' has been deleted successfully"
                    )
                else:
                    logger.error(
                        f"Could not delete event with id '{event.target_event_id[:10]}...'"
                    )

            else:
                error_message = f"Unknown event type of type '{type(event)}': {event}"
                logger.error(error_message)
                raise ValueError(error_message)
