
import logging
_log = logging.getLogger(__name__)

import sqlite3, json, sys

if sys.version_info>=(3,0,0):
    def loads(V):
        try:
            return json.loads(V.decode('ascii'))
        except:
            _log.exception("JSON serialization error: \"%s\""%V)
            raise
    sqlite3.register_converter('json', loads)
else:
    sqlite3.register_converter('json', json.loads)

def connect(fname):
    conn = sqlite3.connect(fname,
                           isolation_level='DEFERRED',
                           detect_types=sqlite3.PARSE_COLNAMES)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        C = conn.cursor()
        C.execute("PRAGMA user_version;")
        ver = C.fetchone()[0]
        if ver==0:
            _log.info("Initialize new database")
            C.executescript(_schema)
        elif ver!=1:
            raise RuntimeError(".db has newer schema version %d"%ver)
        else:
            _log.debug("Use existing database")
        C.execute("PRAGMA user_version=1;")
    except:
        conn.close()
        raise
    else:
        return conn

# We would like to add 'UNIQUE(name, next)' to config,
# but this is difficult for sqlite to handle w/ update and distinct-ness of NULL
#
# so this must be ensured by our logic (cf. storeServiceConfig())
#
#  https://www.sqlite.org/nulls.html

_schema = """
CREATE TABLE config (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  next REFERENCES config(id) ON DELETE CASCADE,
  created TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  desc TEXT NOT NULL,
  system TEXT
);
CREATE INDEX config_name ON config(name);
CREATE INDEX config_name_supercede ON config(name, next);

CREATE TABLE config_pv (
  id INTEGER PRIMARY KEY,
  config REFERENCES config(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  tags TEXT NOT NULL DEFAULT "",
  groupName TEXT NOT NULL DEFAULT "",
  readonly INT NOT NULL DEFAULT 0,
  UNIQUE(config, name)
);
CREATE INDEX config_pv_config ON config_pv(config);
CREATE UNIQUE INDEX config_pv_config_name ON config_pv(config, name);

CREATE TABLE event (
  id INTEGER PRIMARY KEY,
  config REFERENCES config(id) ON DELETE CASCADE NOT NULL,
  created TEXT NOT NULL,
  user TEXT,
  comment TEXT,
  approve INTEGER
);
CREATE INDEX event_config ON event(config);
CREATE INDEX event_config_created ON event(config,created);

CREATE TABLE event_pv (
  id INTEGER PRIMARY KEY,
  event REFERENCES event(id) ON DELETE CASCADE NOT NULL,
  pv REFERENCES config_pv(id) ON DELETE CASCADE NOT NULL,
  dtype INTEGER NOT NULL,
  severity INTEGER NOT NULL,
  status INTEGER NOT NULL,
  time INTEGER NOT NULL,
  timens INTEGER NOT NULL,
  value TEXT NOT NULL,
  UNIQUE(event, pv)
);
CREATE INDEX event_pv_event ON event_pv(event);
CREATE UNIQUE INDEX event_pv_event_pv ON event_pv(event, pv);
"""
