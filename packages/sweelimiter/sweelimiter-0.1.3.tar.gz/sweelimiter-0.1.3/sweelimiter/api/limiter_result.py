class LimiterResult:

    def __init__(
            self,
            limit_applied: bool,
            description: str,
            limit_meta: list
    ):
        self.limit_applied = limit_applied
        self.description = description
        self.limit_meta = limit_meta

    def __repr__(self):
        return f'LimiterResult(' \
               f'limit_applied={self.limit_applied},' \
               f'description={self.description},' \
               f'limit_meta={self.limit_meta}' \
               f')'
