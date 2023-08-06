import io
import unittest

import jsonschema

from installed_packages_diff.config import load_config


class ConfigTest(unittest.TestCase):
  def test_missing_version(self):
    config_yaml = """groups:"""
    with self.assertRaises(jsonschema.exceptions.ValidationError) as ex_ctx:
      load_config(io.StringIO(config_yaml))
    self.assertEqual("'version' is a required property",
                     ex_ctx.exception.message)

  def test_invalid_version(self):
    config_yaml = """version: 'invalid'"""
    with self.assertRaises(jsonschema.exceptions.ValidationError) as ex_ctx:
      load_config(io.StringIO(config_yaml))
    self.assertEqual("'invalid' is not one of ['installed-packages-diff/2']",
                     ex_ctx.exception.message)

  def test_minimal_config(self):
    config_yaml = """version: 'installed-packages-diff/2'"""
    config = load_config(io.StringIO(config_yaml))
    self.assertEqual(0, len(config.groups))

  def test_missing_username(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  db:
    servers:
      - username: user
        hostname: dbdev
      - hostname: dbdev
"""
    config = load_config(io.StringIO(config_yaml))
    self.assertIsNotNone(config.groups[0].servers[0].username)
    self.assertIsNone(config.groups[0].servers[1].username)

  def test_valid_group_type(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  group:
    type: rpm
    servers:
      - hostname: host
        username: root
      - hostname: host
        username: root
        type: dpkg
"""
    config = load_config(io.StringIO(config_yaml))
    self.assertEqual("rpm", config.groups[0].type)
    self.assertEqual("rpm", config.groups[0].servers[0].type)
    self.assertEqual("dpkg", config.groups[0].servers[1].type)

  def test_single_server(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  group:
    servers:
      - hostname: host
        username: root
"""
    with self.assertRaises(jsonschema.exceptions.ValidationError) as ex_ctx:
      load_config(io.StringIO(config_yaml))
    self.assertEqual("[{'hostname': 'host', 'username': 'root'}] is too short",
                     ex_ctx.exception.message)

  def test_missing_hostname(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  db:
    servers:
      - username: root
      - username: root
"""
    with self.assertRaises(jsonschema.exceptions.ValidationError) as ex_ctx:
      load_config(io.StringIO(config_yaml))
    self.assertEqual("'hostname' is a required property",
                     ex_ctx.exception.message)

  def test_expand_username(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  db:
    servers:
      - username: ${USER}
        hostname: host1
      - username: ${USER}
        hostname: host2
"""
    config = load_config(io.StringIO(config_yaml))
    self.assertNotEqual("${USER}", config.groups[0].servers[0].username)
    self.assertNotEqual("${USER}", config.groups[0].servers[1].username)

  def test_expand_hostname(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  db:
    servers:
      - username: user1
        hostname: ${USER}s_machine
      - username: user2
        hostname: ${USER}s_machine
"""
    config = load_config(io.StringIO(config_yaml))
    self.assertNotEqual("${USER}s_machine", config.groups[0].servers[0].hostname)
    self.assertNotEqual("${USER}s_machine", config.groups[0].servers[1].hostname)

  def test_full(self):
    config_yaml = """version: 'installed-packages-diff/2'
groups:
  db:
    servers:
      - username: root
        hostname: dbdev
        excludes:
          - "missing"
      - username: root
        hostname: dblive
  web:
    servers:
      - username: root
        hostname: webdev
        excludes:
          - "missing"
      - username: root
        hostname: weblive
"""
    config = load_config(io.StringIO(config_yaml))
    self.assertEqual([g.name for g in config.groups], ["db", "web"])
    self.assertEqual(
      [(s.hostname, s.username) for s in config.groups[1].servers],
      [("webdev", "root"), ("weblive", "root")])
    self.assertEqual(config.groups[1].servers[0].excludes, {"missing"})
    self.assertEqual(config.groups[1].servers[1].excludes, set())
