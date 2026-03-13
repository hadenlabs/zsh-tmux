# Troubleshooting

## Environment

### Validation environment issues

This repository uses `uv` and `task`, not poetry. If validation or formatting commands fail because the environment is incomplete, run:

```{.bash}
task environment
```

Then rerun:

```{.bash}
task validate
```
