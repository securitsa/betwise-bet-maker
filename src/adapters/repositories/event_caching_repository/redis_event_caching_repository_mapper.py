from domain.entities.event import Event


class RedisEventCachingRepositoryMapper:
    @staticmethod
    def to_event_entity(event: dict) -> Event:
        return Event(
            name=event.get("name"),
            coefficient=event.get("coefficient"),
            expiration_at=event.get("expiration_at"),
            status=event.get("status"),
            token=event.get("token"),
            description=event.get("description"),
            created_at=event.get("created_at"),
            status_updated_at=event.get("status_updated_at"),
        )
