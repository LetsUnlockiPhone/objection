from ..commands import (
    filemanager,
    frida_commands,
    fridascript,
    memory,
    device,
    sqlite,
    keychain,
    ui,
    hooking,
    jobs,
    plist,
    cookies,
    nsuserdefaults,
    pasteboard,
    pinning
)

from ..utils.helpers import (
    list_files_in_current_fm_directory,
    list_folders_in_current_fm_directory,
    list_current_jobs
)

# commands are defined with their name being the key, then optionally
# have a meta, dynamic and commands key.
COMMANDS = {
    'commands': {

        '!': {
            'meta': 'Execute an Operating System command',
            'help': (
                'Command: !\n'
                '\n'
                'Usage: !<shell command>\n'
                '\n'
                'Executes operating system commands using pythons Subprocess\n'
                'modules.\n'
                'Commands that have caused an error, or when there is output to\n'
                'display from stderr, will show in red. Commands that have output\n'
                'that was sent to stdout will display in white.\n'
                '\n'
                'Examples:\n'
                '   !ls\n'
                '   !uname -a'
            ),
            'exec': None,  # handled in the Repl class itself
        },

        'reconnect': {
            'meta': 'Reconnect to the current device',
            'help': (
                'Command: reconnect\n'
                '\n'
                'Usage: reconnect\n'
                '\n'
                'Attempts to reconnect to the Frida Gadget specified with --gadget on startup.\n'
                'The connection mode (ie: usb / network) can not be changed unless the repl\n'
                'is restarted.\n'
                '\n'
                'Examples:\n'
                '   reconnect\n'
            ),
            'exec': None,  # handled in the Repl class itself
        },

        'import': {
            'meta': 'Import fridascript from a full path',
            'help': (
                'Command: import\n'
                '\n'
                'Usage: import <path to local fridascript> (optional: <job name>)\n'
                '\n'
                'Imports Fridascript from a file on the local filesystem and executes it as a job.\n'
                'To \'unload\' the script, the job that was started to should be killed.\n'
                'You can list all of the current jobs using the `jobs list` command. If no name was\n'
                'specified for your job, a generic name of \'user-script\' will be used for the \n'
                'job started as a result of the import.\n'
                '\n'
                'Examples:\n'
                '   import ~/home/myscript.js\n'
                '   import ~/home/hooks/custom.js custom-hook-name'
            ),
            'exec': fridascript.load
        },

        # file manager commands

        'cd': {
            'meta': 'Change the current working directory',
            'help': (
                'Command: cd\n'
                '\n'
                'Usage: cd <directory on remote device>\n'
                '\n'
                'Changes the current working directory on the device.\n'
                'Many commands within objection are mindful and aware of the current\n'
                'working directory. An example of this includes the sqlite command, that\n'
                'allows you to connect to a file in the current path, or to a file specified\n'
                'with a full path relative to root (/).\n'
                'For more directories that are applicable to the current app, inspect the\n'
                'output of the `env` command.\n'
                '\n'
                'Examples:\n'
                '   cd Library/Caches\n'
                '   cd Preferences\n'
                '   cd /'
            ),
            'dynamic': list_folders_in_current_fm_directory,
            'exec': filemanager.cd
        },

        'ls': {
            'meta': 'List files in the current working directory',
            'help': (
                'Command: ls\n'
                '\n'
                'Usage: ls (optional: <directory on remote device>)\n'
                '\n'
                'Display the contents of a directory on the mobile device. The output details\n'
                'the permissions of the directory in question, as well as those for each file\n'
                'and directory within. If no directory is specified, the current working \n'
                'directory is assumed and listed.\n'
                '\n'
                'Examples:\n'
                '   ls Library/Caches\n'
                '   ls /\n'
                '   ls'
            ),
            'exec': filemanager.ls,
        },

        'pwd': {
            'meta': 'Work with the current directory',
            'help': (
                'Contains subcommands to work with the current working directory\n'
                'on the device.'
            ),
            'commands': {
                'print': {
                    'meta': 'Print the current working directory on the device',
                    'help': (
                        'Command: pwd print\n'
                        '\n'
                        'Usage: pwd print\n'
                        '\n'
                        'Display the current working directory.\n'
                        '\n'
                        'Examples:\n'
                        '   pwd print'
                    ),
                    'exec': filemanager.pwd_print
                },
            },
        },

        'upload': {
            'meta': 'Upload a file',
            'help': (
                'Command: upload\n'
                '\n'
                'Usage: upload <local source file> <remove destination>\n'
                '\n'
                'Upload a file from the local filesystem to the remote filesystem.\n'
                'If a full path is not specified for the remote destination, the current\n'
                'working directory is assumed as the relative directory for the upload\n'
                'destination.\n'
                'If the file already exists on the remote filesystem, it will be overridden.\n'
                '\n'
                'Examples:\n'
                '   upload test.sqlite Document/Preferences/test.sqlite'
            ),
            'exec': filemanager.upload
        },

        'download': {
            'meta': 'Download a file',
            'help': (
                'Command: download\n'
                '\n'
                'Usage: download <remote location> <local destination>\n'
                '\n'
                'Download a file from a location on the mobile device, to a local destination.\n'
                '\n'
                'Examples:\n'
                '   download Document/Preferences/test.sqlite test.sqlite'
            ),
            'dynamic': list_files_in_current_fm_directory,
            'exec': filemanager.download
        },

        # device and env info commands

        'env': {
            'meta': 'Print information about the environment',
            'help': (
                'Command: env\n'
                '\n'
                'Usage: env\n'
                '\n'
                'Display information about the current environment.\n'
                'On iOS devices, this includes the location of the current applications bundle,\n'
                'the Documents/ and Library/ directory.'
                '\n'
                'Examples:\n'
                '   env'
            ),
            'exec': device.get_environment
        },

        'frida': {
            'meta': 'Get information about the Frida environment',
            'help': (
                'Command: frida\n'
                '\n'
                'Usage: frida\n'
                '\n'
                'Displays information about Frida. This includes the version of the Frida gadget,\n'
                'process architecture and platform.\n'
                '\n'
                'Examples:\n'
                '   frida'
            ),
            'exec': frida_commands.frida_environment
        },

        # memory commands

        'memory': {
            'meta': 'Work with the current processes memory',
            'help': (
                'Contains subcommands to work with memory within the current process.\n'
                'Examples include commands to dump the current process memory, dump\n'
                'the memory of a specific loaded module, list exported modules or\n'
                'write raw bytes to memory addresses.'
            ),

            'commands': {
                'dump': {
                    'meta': 'Commands to dump parts of the processes memory',
                    'help': (
                        'Contains subcommands to dump process memory'
                    ),

                    'commands': {
                        'all': {
                            'meta': 'Dump the entire memory of the current process',
                            'help': (
                                'Command: memory dump all\n'
                                '\n'
                                'Usage: memory dump all <local destination>\n'
                                '\n'
                                'Dumps all of the current processes\' memory that is marked as readable and\n'
                                'writable (rw-) to a file specified by local destination.\n'
                                '\n'
                                'Examples:\n'
                                '   memory dump all process_memory.dmp'
                            ),
                            'exec': memory.dump_all
                        },

                        'from_base': {
                            'meta': 'Dump (x) bytes of memory from a base address to file',
                            'help': (
                                'Command: memory dump all\n'
                                '\n'
                                'Usage: memory dump <base address> <size to dump> <local destination>\n'
                                '\n'
                                'Dumps memory from within the current process from a base address, for a set number\n'
                                'of bytes to a local file specified by local destination. For example addresses and\n'
                                'sizes, the `memory list modules` command may be used.\n'
                                'Specifying addresses or sizes that are outside of the current processes sandbox\n'
                                'has a *high* chance of crashing the application. Use with caution.\n'
                                '\n'
                                'Examples:\n'
                                '   memory dump from_base 0x10009c000 442368 main\n'
                                '   memory dump from_base 0x10f88e000 548864 CoreAudio'
                            ),
                            'exec': memory.dump_from_base
                        }
                    },
                },

                'list': {
                    'meta': 'List memory related information about the current process',
                    'help': (
                        'Contains subcommands to list modules and module exports.'
                    ),
                    'commands': {

                        'modules': {
                            'meta': 'List loaded modules in the current process',
                            'help': (
                                'Command: memory list modules\n'
                                '\n'
                                'Usage: memory list modules\n'
                                '\n'
                                'List all of the modules loaded in the current process, detailing their base\n'
                                'address, size and location on disk.\n'
                                '\n'
                                'Examples:\n'
                                '   memory list modules'
                            ),
                            'exec': memory.list_modules
                        },

                        'exports': {
                            'meta': 'List the exports of a module',
                            'help': (
                                'Command: memory list exports\n'
                                '\n'
                                'Usage: memory list exports <module name>\n'
                                '\n'
                                'List exports in a specific loaded module. Exports found using this command\n'
                                'could be used in Fridascripts to hook with module.findExportByName().\n'
                                'For a list of modules to list exports from the `memory list modules` command\n'
                                'may be used.\n'
                                '\n'
                                'Examples:\n'
                                '   memory list exports libsystem_configuration.dylib\n'
                                '   memory list exports UserManagement'
                            ),
                            'exec': memory.dump_exports
                        }
                    },
                },

                'search': {
                    'meta': 'Search for pattern in the applications memory',
                    'help': (
                        'Command: memory search\n'
                        '\n'
                        'Usage: memory search "<pattern>" (optional: --string)\n'
                        '\n'
                        'Search the current processes\' heap for a pattern. A pattern is represented by a\n'
                        'byte sequence such as eb ff aa. It is also possible to specify wildcards such as\n'
                        'eb ff ?? aa, indicating that you are looking for a pattern that starts with eb ff,\n'
                        'has any other byte and then has aa.\n'
                        'It is also possible to  provide a raw string, which should be suffixed with the\n'
                        '--string flag, indicating to the command that it should convert the string to\n'
                        'bytes before executing the search. Wildcards are not supported in string searches.\n'
                        '\n'
                        'Examples:\n'
                        '   memory search "41 41 41 41"\n'
                        '   memory search "41 ?? de ad"\n'
                        '   memory search "deadbeef" --string'
                    ),
                    'exec': memory.find_pattern
                },

                'write': {
                    'meta': 'Write raw bytes to a memory address. Use with caution!',
                    'help': (
                        'Command: memory write\n'
                        '\n'
                        'Usage: memory write "<address>" "<pattern>" (optional: --string)\n'
                        '\n'
                        'Write an arbitrary set of bytes to an address in memory. Using this command has a high\n'
                        'chance of crashing the applications process if you attempt to write to adresses outside\n'
                        'of the applications heap, or your bytes specified cause to go outside of some memory\n'
                        'boundary.\n'
                        '\n'
                        'Examples:\n'
                        '   memory write 0x117a2e347 "ff 41 41 42"'
                    ),
                    'exec': memory.write
                }
            },
        },

        # sqlite commands
        'sqlite': {
            'meta': 'Work with SQLite databases',
            'help': (
                'Contains subcommands to work with SQLite databases on the remote device.\n'
                'Connecting to a SQLite database will result in a copy of the database from\n'
                'the remote device being downloaded locally. All queries that are run will\n'
                'be run on the locally cached database. If the changes need to be available\n'
                'on the remote device, the database should be `sync`\'ed back.'
            ),

            'commands': {
                'status': {
                    'meta': 'Show the status of the SQLite database connection',
                    'help': (
                        'Command: sqlite status\n'
                        '\n'
                        'Usage: sqlite status\n'
                        '\n'
                        'Check the status of the SQLite connection. Outputs the the locally cached\n'
                        'location as well as the remote source it was cached from.\n'
                        '\n'
                        'Examples:\n'
                        '   sqlite status'
                    ),
                    'exec': sqlite.status
                },

                'connect': {
                    'meta': 'Connect to a SQLite database (file)',
                    'help': (
                        'Command: sqlite connect\n'
                        '\n'
                        'Usage: sqlite connect <remote sqlite database location>\n'
                        '\n'
                        'Connect to a SQLite database on the remote device. The connection process downloads\n'
                        'a copy of the remote database file to a local temporary directory. The file is then\n'
                        'validated to make sure that it is a SQLite3 database file. Once considered a valid\n'
                        'database file, the connection is considered complete.\n'
                        'The `sqlite status` command will show details about the connection once successful.\n'
                        '\n'
                        'Examples:\n'
                        '   sqlite connect Preferences/settings.sqlite\n'
                        '   sqlite connect credentials.sqlite'
                    ),
                    'dynamic': list_files_in_current_fm_directory,
                    'exec': sqlite.connect
                },
                'disconnect': {
                    'meta': 'Disconnect from a SQLite database (file)',
                    'help': (
                        'Command: sqlite disconnect\n'
                        '\n'
                        'Usage: sqlite disconnect\n'
                        '\n'
                        'Disconnect from the currently connected SQLite database file. This command will clean\n'
                        'the locally cached version of the database file. If you made changes you want to save,\n'
                        'run the `sqlite sync` command before disconnecting. This command is also run if the\n'
                        'REPL is existed.\n'
                        '\n'
                        'Examples:\n'
                        '   sqlite disconnect'
                    ),
                    'exec': sqlite.disconnect
                },
                'execute': {
                    'meta': 'Execute SQLite statements on the connected database',
                    'help': (
                        'Contains subcommands to execute queries against a connected SQLite database.'
                    ),
                    'commands': {
                        'schema': {
                            'meta': 'Dump the schema of the connected database',
                            'help': (
                                'Command: sqlite execute schema\n'
                                '\n'
                                'Usage: sqlite execute schema\n'
                                '\n'
                                'Get the database schema for the currently connected SQLite database.\n'
                                '\n'
                                'Examples:\n'
                                '   sqlite execute schema'
                            ),
                            'exec': sqlite.schema
                        },
                        'query': {
                            'meta': 'Execute a query on the connected SQLite database',
                            'help': (
                                'Command: sqlite execute query\n'
                                '\n'
                                'Usage: sqlite execute query <sql query>\n'
                                '\n'
                                'Execute a query against the cached copy of the connected SQLite database.\n'
                                'If your changes need to be effective on the device, execute the `sqlite sync`\n'
                                'command to upload the modified database back to the device.\n'
                                '\n'
                                'Examples:\n'
                                '   sqlite execute query select * from data;\n'
                                '   sqlite execute query delete from data;'
                            ),
                            'exec': sqlite.execute
                        },
                    }
                },
                'sync': {
                    'meta': 'Sync the locally cached SQLite database with one on the device',
                    'help': (
                        'Command: sqlite sync\n'
                        '\n'
                        'Usage: sqlite sync\n'
                        '\n'
                        'Sync the locally cached SQLite database with the remote database.\n'
                        'Any changes made since the last `sqlite connect` will be available on the\n'
                        'device post-sync.\n'
                        '\n'
                        'Examples:\n'
                        '   sqlite sync'
                    ),
                    'exec': sqlite.sync
                }
            }
        },

        # jobs commands
        'jobs': {
            'meta': 'Work with objection jobs',
            'help': (
                'Contains subcommands to work with objection jobs. This includes listing and killing them.'
            ),
            'commands': {
                'list': {
                    'meta': 'List all of the current jobs',
                    'help': (
                        'Command: jobs list\n'
                        '\n'
                        'Usage: jobs list\n'
                        '\n'
                        'List the currently running jobs. Jobs are asynchronous Fridascripts that were\n'
                        'submitted and have not yet been unloaded from the process. Examples of such\n'
                        'jobs include the iOS method argument dumper and pasteboard monitor. To unload\n'
                        'a job, the `jobs kill <jobid>` command may be used.\n'
                        '\n'
                        'Examples:\n'
                        '   jobs list'
                    ),
                    'exec': jobs.show
                },
                'kill': {
                    'meta': 'Kill a job. This unloads the script',
                    'help': (
                        'Command: jobs kill\n'
                        '\n'
                        'Usage: jobs kill <job uuid>\n'
                        '\n'
                        'Kills a running job identified by its UUID. When a job is killed, objection will\n'
                        'unload the Fridascript from the process\' memory.'
                        '\n'
                        'Examples:\n'
                        '   jobs kill 9415c4c7-2824-46a5-8539-d2d35ba2158c'
                    ),
                    'dynamic': list_current_jobs,
                    'exec': jobs.kill
                }
            }
        },

        # generic ui commands
        'ui': {
            'meta': 'Generic user interface commands',
            'help': (
                'Contains subcommands that interact with the applications user interface.'
            ),
            'commands': {
                'alert': {
                    'meta': 'Show an alert message, optionally specifying the message to show. (Currently crashes iOS)',
                    'help': (
                        'Command: ui alert\n'
                        '\n'
                        'Usage: ui alert (optional: "<alert message>")\n'
                        '\n'
                        'Displays an alert popup on iOS devices, or a Toast message on Android devices.\n'
                        'This is useful to demonstrate that the application was successfully hooked. Providing\n'
                        'an alert message will display that message instead of the default.\n'
                        'Note: Currently, once the iOS alert message has been displayed, dismissing the message\n'
                        'unfortunately crashes the application.\n'
                        '\n'
                        'Examples:\n'
                        '   ui alert\n'
                        '   ui alert \'custom message!\''
                    ),
                    'exec': ui.alert
                }
            }
        },

        # ios commands
        'ios': {
            'meta': 'Commands specific to iOS',
            'help': (
                'Contains subcommands to work with iOS specific features. These include features\n'
                'such as keychain dumping, reading plists and bypassing SSL pinning.'
            ),
            'commands': {
                'keychain': {
                    'meta': 'Work with the iOS keychain',
                    'help': (
                        'Contains subcommands to work with the iOS keychain.'
                    ),
                    'commands': {
                        'dump': {
                            'meta': 'Dump the keychain for the current app',
                            'help': (
                                'Command: ios keychain dump\n'
                                '\n'
                                'Usage: ios keychain dump (optional: --json <filename>)\n'
                                '\n'
                                'Extracts the keychain items for the current process. This is achieved by iterating\n'
                                'over the keychain type classes available in iOS and populating a search dictionary\n'
                                'with them. This dictionary is then used as a query to SecItemCopyMatching() and the\n'
                                'results parsed.\n'
                                'Providing a filename with the --json flag will dump all of the keychain attributes\n'
                                'to the file specified for later inspection.\n'
                                '\n'
                                'Examples:\n'
                                '   ios keychain dump\n'
                                '   ios keychain dump --json keychain.json'
                            ),
                            'exec': keychain.dump
                        }
                    }
                },
                'plist': {
                    'meta': 'Work with iOS Plists',
                    'help': (
                        'Contains subcommands to work with iOS Plist entries.'
                    ),
                    'commands': {
                        'cat': {
                            'meta': 'Cat a plist',
                            'help': (
                                'Command: ios plist cat\n'
                                '\n'
                                'Usage: ios plist cat <remote plist filename>\n'
                                '\n'
                                'Parses and echoes a plist file on the remote iOS device to screen. If this\n'
                                'parsing is not sufficient, one can always `download` the plist file itself\n'
                                'for parsing using other tools.\n'
                                '\n'
                                'Examples:\n'
                                '   ios plist cat Info.plist\n'
                            ),
                            'dynamic': list_files_in_current_fm_directory,
                            'exec': plist.cat
                        }
                    }
                },
                'nsuserdefaults': {
                    'meta': 'Work with NSUserDefaults',
                    'help': (
                        'Contains subcommands to work with the iOS NSUserDefaults class.'
                    ),
                    'commands': {
                        'get': {
                            'meta': 'Get all of the entries',
                            'help': (
                                'Command: ios nsuserdefaults get\n'
                                '\n'
                                'Usage: ios nsuserdefaults get\n'
                                '\n'
                                'Queries the applications NSUserDefaults class for all of the entries in\n'
                                'the current application bundle and echoes the entries to screen.\n'
                                '\n'
                                'Examples:\n'
                                '   ios nsuserdefaults get\n'
                            ),
                            'exec': nsuserdefaults.get
                        }
                    }
                },
                'cookies': {
                    'meta': 'Work with shared cookies',
                    'help': (
                        'Contains subcommands to work with iOS shared cookies.'
                    ),
                    'commands': {
                        'get': {
                            'meta': 'Get the current apps shared cookies',
                            'help': (
                                'Command: ios cookies get\n'
                                '\n'
                                'Usage: ios cookies get\n'
                                '\n'
                                'Queries iOS\'s NSHTTPCookieStorage class, extracting cookie values out of the\n'
                                'sharedHTTPCookieStorage. Various URL fetching methods use the\n'
                                'sharedHTTPCookieStorage to store cookie data. This information may be useful\n'
                                'to get session cookies for web services to reuse in other tools/browsers.\n'
                                '\n'
                                'Examples:\n'
                                '   ios cookies get\n'
                            ),
                            'exec': cookies.get
                        }
                    }
                },
                'ui': {
                    'meta': 'iOS user interface commands',
                    'help': (
                        'Contains subcommands to interact with the iOS user interface. This includes commands\n'
                        'to dump the current view hierarchy as well as bypassing screens that require TouchID\n'
                        'to proceed.'
                    ),
                    'commands': {
                        'alert': {
                            'meta': ('Show an alert message, optionally specifying the message to'
                                     'show. (Currently crashes iOS)'),
                            'help': (
                                'Command: ios ui alert\n'
                                '\n'
                                'Usage: ios ui alert (optional: "<alert message>")\n'
                                '\n'
                                'Displays an alert popup on an iOS device. A message to display may be specified\n'
                                'optionally.\n'
                                '\n'
                                'Examples:\n'
                                '   ios ui alert\n'
                                '   ios ui alert \'my message±\''
                            ),
                            'exec': ui.alert
                        },
                        'dump': {
                            'meta': 'Dump the serialized UI',
                            'help': (
                                'Command: ios ui dump\n'
                                '\n'
                                'Usage: ios ui dump\n'
                                '\n'
                                'Dumps the current, serialized user interface. This is useful to see which values\n'
                                'or classes may be attached to UI elements.\n'
                                '\n'
                                'Examples:\n'
                                '   ios ui alert\n'
                                '   ios ui alert \'my message\''
                            ),
                            'exec': ui.dump_ios_ui
                        },
                        'screenshot': {
                            'meta': 'Screenshot the current UIView',
                            'help': (
                                'Command: ios ui screenshot\n'
                                '\n'
                                'Usage: ios ui screenshot <local png destination>\n'
                                '\n'
                                'Screenshots the current foregrounded UIView and saves it as a PNG locally.\n'
                                'Note: Does not work at the moment, may actually need a jailbroken device.\n'
                                '\n'
                                'Examples:\n'
                                '   ios ui screenshot screenshot.png'
                            ),
                            'exec': ui.ios_screenshot
                        },
                        'touchid_bypass': {
                            'meta': 'Hook the iOS TouchID class and respond with successful fingerprints',
                            'help': (
                                'Command: ios ui touchid_bypass\n'
                                '\n'
                                'Usage: ios ui touchid_bypass\n'
                                '\n'
                                'Hooks into the -[LAContext evaluatePolicy:localizedReason:reply:] selector and\n'
                                'replies with a successful message from the operating system when a touchID prompt\n'
                                'is dismissed. This is useful in cases where the application relies solely on the\n'
                                'operating system to tell it if a fingerprint read was successful or not.\n'
                                'Note: This does *not* bypass cases where TouchID is needed to decrypt a keychain\n'
                                'entry, simply because the actual data itself is not stored in the keychain but\n'
                                'instead lives in the Secure Enclave. The keychain simply contains a token to the\n'
                                'data itself.\n'
                                '\n'
                                'Examples:\n'
                                '   ios ui touchid_bypass'
                            ),
                            'exec': ui.bypass_touchid
                        }
                    }
                },
                'hooking': {
                    'meta': 'Commands used for hooking methods in iOS',
                    'help': (
                        'Contains subcommands helpful when developing custom hooks. This includes discovery\n'
                        'of Objective-C classes and methods in those classes, as well as dumping method\n'
                        'arguments as they are called in real time.'
                    ),
                    'commands': {
                        'list': {
                            'meta': 'Lists various bits of information',
                            'help': (
                                'Contains subcommands to list various bits of information, such as Objectu'
                            ),
                            'commands': {
                                'classes': {
                                    'meta': 'List classes available in the current application',
                                    'help': (
                                        'Command: ios hooking list classes\n'
                                        '\n'
                                        'Usage: ios hooking list classes (optional: --ignore-native)\n'
                                        '\n'
                                        'Lists all of the classes in the current Objective-C runtime. Specifying\n'
                                        'the --ignore-native flag, filters out classes with common prefixes such as\n'
                                        '\'NS\' and \'CF\'.\n'
                                        '\n'
                                        'Examples:\n'
                                        '   ios hooking list classes'
                                        '   ios hooking list classes --ignore-native'
                                    ),
                                    'exec': hooking.show_ios_classes
                                },
                                'class_methods': {
                                    'meta': 'List the methods in a class',
                                    'exec': hooking.show_ios_class_methods
                                }
                            }
                        },
                        'dump': {
                            'meta': 'Dumps various bits of information',
                            'help': (
                                'Contains subcommands to dump various bits of information, such as realtime\n'
                                'method arguments used when a specific method was invoked.'
                            ),
                            'commands': {
                                'method_args': {
                                    'meta': 'Attempt to dump arguments for a given method',
                                    'help': (
                                        'Command: ios hooking dump method_args\n'
                                        '\n'
                                        'Usage: ios hooking dump method_args <+/-> <class_name> <method_name>\n'
                                        '\n'
                                        'Dumps method invocations in real time, including the arguments used at the\n'
                                        'time. This command tries its best to convert the arguments themselves into\n'
                                        'readable data, but sometimes the pointers used are to data structures not\n'
                                        'easily converted to readable formats.\n'
                                        '\n'
                                        'When issuing this command, a few bits of information is needed to build up\n'
                                        'the full class that should be hooked. The needed information includes:\n'
                                        '   - A \'+\' or \'-\' indicating a class or instance method\n'
                                        '   - The ClassName in question\n'
                                        '   - The method name *including* the argument separators (\':\')\n'
                                        '\n'
                                        'All of the information you need can be sourced with the `ios hooking list *`\n'
                                        'commands, or using the \'class-dump\' tool.\n'
                                        '\n'
                                        'Examples:\n'
                                        '   ios hooking dump method_args + KeychainDataManager find:\n'
                                        '   ios hooking dump method_args - PinnedNSURLSessionStarwarsApi'
                                        ' getJsonResponseFrom:onSuccess:onFailure:'
                                    ),
                                    'exec': hooking.dump_ios_method_args
                                }
                            }
                        },
                        'watch': {
                            'meta': 'Watch invocations of classes and methods',
                            'help': (
                                'Contains subcommands to watch for method invocations on Objective-C classes.'
                            ),
                            'commands': {
                                'class': {
                                    'meta': 'Hook all methods in a class and report on invocations',
                                    'help': (
                                        'Command: ios hooking watch class\n'
                                        '\n'
                                        'Usage: ios hooking watch <class_name> (--include-parents)\n'
                                        '\n'
                                        'Hooks into all of the methods available in the Objective-C class specified\n'
                                        'by class_name and reports on invocations of any methods contained within.\n'
                                        'If the --include-parents flag is specified, all methods inherited from a\n'
                                        'parent class will also be hooked and reported on.\n'
                                        '\n'
                                        'Examples:\n'
                                        '   ios hooking watch KeychainDataManager\n'
                                        '   ios hooking watch PinnedNSURLSessionStarwarsApi --include-parents'
                                    ),
                                    'exec': hooking.watch_class
                                },
                                'method': {
                                    'meta': 'Hook a specific method and report on invocations',
                                    'help': (
                                        'Command: ios hooking watch method\n'
                                        '\n'
                                        'Usage: ios hooking method "<full class & selector>"\n'
                                        '\n'
                                        'Hooks into a specified Objective-C method and reports on invocations.\n'
                                        'A full class and method is expected, including whether its an instance\n'
                                        'or class method.\n'
                                        '\n'
                                        'Examples:\n'
                                        '   ios hooking watch method "+[KeychainDataManager update:forKey:]\n'
                                        '   ios hooking watch method "-[PinnedNSURLSessionStarwarsApi '
                                        'getJsonResponseFrom:onSuccess:onFailure:]"'
                                    ),
                                    'exec': hooking.watch_class_method
                                }
                            }
                        }
                    }
                },
                'pasteboard': {
                    'meta': 'Work with the iOS pasteboard',
                    'help': (
                        'Contains subcommands to work with the iOS pasteboard.'
                    ),
                    'commands': {
                        'monitor': {
                            'meta': 'Monitor the iOS pasteboard',
                            'help': (
                                'Command: ios pasteboard monitor\n'
                                '\n'
                                'Usage: ios pasteboard monitor\n'
                                '\n'
                                'Hooks into the iOS UIPasteboard class and polls the generalPasteboard every\n'
                                '5 seconds for data. If new data is found, different from the previous poll,\n'
                                'that data will be dumped to screen.\n'
                                '\n'
                                'Examples:\n'
                                '   ios pasteboard monitor'
                            ),
                            'exec': pasteboard.monitor
                        }
                    }
                },
                'sslpinning': {
                    'meta': 'Work with iOS SSL pinning',
                    'help': (
                        'Contains subcommands to work with iOS SSL pinning related calls.'
                    ),
                    'commands': {
                        'disable': {
                            'meta': 'Attempt to disable SSL pinning in various iOS libraries/classes',
                            'help': (
                                'Command: ios sslpinning disable\n'
                                '\n'
                                'Usage: ios sslpinning disable\n'
                                '\n'
                                'Attempts to disable SSL Pinning on iOS devices. This is achieved by hooking\n'
                                'into methods commonly used by Frameworks and Libraries such as AFNetworking,\n'
                                'NSURLSession and the now deprecated NSURLConnection.\n'
                                'This command also implements the bypass techniques used in the well-known\n'
                                'SSL-Killswitch2 app, including a new technique reportedly working in iOS10.\n'
                                '\n'
                                'If this method does not disable the applications SSL pinning implementation,\n'
                                'then it may still be possible to bypass it via \'helper\' methods commonly\n'
                                'used by developers to help when testing in development / staging environments.\n'
                                'Be on the lookout for classes / methods that relate to pinning that may simply\n'
                                'return a BOOL value.\n'
                                '\n'
                                'Examples:\n'
                                '   ios sslpinning disable'
                            ),
                            'exec': pinning.ios_disable
                        }
                    }
                }
            }
        },

        'exit': {
            'meta': 'Exit',
        },
    }
}