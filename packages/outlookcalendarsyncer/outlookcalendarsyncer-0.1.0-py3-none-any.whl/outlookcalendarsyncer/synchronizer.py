import logging
import re
from typing import List

from outlookcalendarsyncer.outlook import (
    OfficeAccount,
    CalendarEvent,
    NewEventChangeEvent,
    ModifiedEventChangeEvent,
    DeletedEventChangeEvent,
    CalendarChangeEvent,
)

logger: logging.Logger = logging.getLogger(__name__)


def filter_events(
        events: List[CalendarEvent], exclude_subjects: List[str]
) -> List[CalendarEvent]:
    exclude_regexps = [re.compile(exclude_rule) for exclude_rule in exclude_subjects]

    def should_exclude(event):
        for exclude_rule in exclude_regexps:
            if exclude_rule.match(event.subject):
                return True
        return False

    return [event for event in events if not should_exclude(event)]


def calculate_difference(
        source_events1: List[CalendarEvent], target_events: List[CalendarEvent]
) -> list[CalendarChangeEvent]:
    def is_event_changed(
            target_event: CalendarEvent, source_event: CalendarEvent
    ) -> bool:
        return (
                target_event.show_as != source_event.show_as
                or target_event.start != source_event.start
                or target_event.end != source_event.end
        )

    synthetic_target_events = {
        event.synthetic_hash: event
        for event in target_events
        if event.synthetic_hash is not None
    }

    source_events = {
        event.id: event for event in source_events1 if event.synthetic_hash is None
    }

    new_events: list[CalendarChangeEvent] = [
        NewEventChangeEvent(
            id=source_event.id,
            subject=source_event.subject,
            show_as=source_event.show_as,
            start=source_event.start,
            end=source_event.end,
        )
        for source_event in source_events.values()
        if source_event.id not in synthetic_target_events
    ]
    changed_events = [
        ModifiedEventChangeEvent(
            target_event_id=target_event.id,
            new_subject=source_event.subject,
            new_show_as=source_event.show_as,
            new_start=source_event.start,
            new_end=source_event.end,
        )
        for target_event in synthetic_target_events.values()
        if (source_event := source_events.get(target_event.synthetic_hash))
           and is_event_changed(target_event, source_event)
    ]
    cancelled_events = [
        DeletedEventChangeEvent(target_event.id)
        for target_event in synthetic_target_events.values()
        if target_event.synthetic_hash not in source_events
    ]

    return new_events + changed_events + cancelled_events


def synchronize_calendars(
        source_account: OfficeAccount, target_account: OfficeAccount, sync_duration: int
):
    logger.info("Retrieving calendar events from source account...")
    source_events = filter_events(
        source_account.list_calendar_events(sync_duration),
        source_account.configuration.exclude_subjects,
    )
    logger.debug(f"Calendar event from source account:")
    for event in source_events:
        logger.debug(f"    {event}")

    logger.info("Retrieving calendar events from target account...")
    target_events = filter_events(
        target_account.list_calendar_events(sync_duration),
        target_account.configuration.exclude_subjects,
    )
    logger.debug(f"Calendar event from target account:")
    for event in target_events:
        logger.debug(f"    {event}")

    logger.info("Calculating different between two calendars...")
    change_events = calculate_difference(source_events, target_events)
    logger.debug(f"Calculated calendar changes:")
    for event in change_events:
        logger.debug(f"    {event}")

    if len(change_events) != 0:
        logger.info(
            f"There are {len(change_events)} change(s) that I'm going to synchronize..."
        )
        target_account.save_calendar_events(
            change_events, source_account.configuration.event_prefix
        )
    else:
        logger.info(
            "All calendar events from source account have been already synced into target account"
        )
