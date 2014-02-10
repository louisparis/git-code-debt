
import collections
import re

import staticconf.getters

from git_code_debt_util.config import get_config_watcher


CONFIG_NAMESPACE = 'metric_config'
metric_config_watcher = get_config_watcher(
    'metric_config.yaml',
    CONFIG_NAMESPACE,
)


class Group(collections.namedtuple('Group', ['name', 'metrics', 'metric_expressions'])):
    __slots__ = ()

    def contains(self, metric_name):
        return (
            metric_name in self.metrics or
            any(expr.search(metric_name) for expr in self.metric_expressions)
        )

    @classmethod
    def from_yaml(cls, name, metrics, metric_expressions):
        return cls(
            name,
            set(metrics),
            tuple(re.compile(expr) for expr in metric_expressions),
        )


def _get_groups_from_yaml(yaml):
    # A group dict maps it's name to a dict containing metrics and
    # metric_expressions
    # Here's an example yaml:
    # [{'Bar': {'metrics': ['Foo', 'Bar'], 'metric_expressions': ['^Baz']}}]
    return tuple(
        Group.from_yaml(*group_dict.keys(), **group_dict.values()[0])
        for group_dict in yaml
    )


groups = staticconf.getters.build_getter(
    _get_groups_from_yaml,
    getter_namespace='metric_config',
)('Groups')
