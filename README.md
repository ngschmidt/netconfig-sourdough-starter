# Network Device Builder

## Goal

Construct a network configuration from basic facts (`kinds`) and a configuration template.

## Overview

### Validation

Intuitively providing a way to validate what's missing in a device definition is pretty important. Dumping a starter file is even better.

### Unit Testing

We want to construct *and automatically test* any non-factory (e.g. not provided by Jinja) capabilities to ensure quality is up to snuff. The approach here *MUST* be eminently testable.

This will be achieved by performing an end-to-end test against truth tables - all `kinds` should be iterable, providing the following objects under `testing`:

```bash
{{ kind }}-test.yml
{{ kind }}-truth.txt
```

This is required to ensure that end-results are consistent, and isn't just a test of code provided in this repository - if a dependency breaks, we'll see it in a pipeline prior to production usage.

### Hardware Portfolio

Located in `kinds`. The eventual goal here is to use YAML Front Matter (YFM) to document `kinds` in-line as a markdown file.

## HOWTO

Generate your `kind` device definition starter:

```bash
python3 net-starter.py -gen-kind {{ kind }}
```

Add your variables, then run again:

```bash
python3 net-starter.py -i {{ variablefile }}
```

Ideally, store the variable file in a source of truth like [Netbox](https://netbox.readthedocs.io/en/stable/) for safe keeping!

## Dependencies

* `cerberus`
* `jinja2`
* `JSON`
* `ruamel.YAML`
