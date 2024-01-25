STATUS_TRANSITIONS = {
    "accurate_edit": {
        "statuses": {
            "start": {
                "message": "Starting Accurate Edit",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-play",
                "color": "#2196F3"
            },
            "too_many_primary": {
                "message": "Too many primary assets listed",
                "group": "Accurate Edit Module",
                "icon": "fa-sharp fa-solid fa-files",
                "color": "red"
            },
            "missing_file": {
                "message": "Too many primary assets listed",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-file-slash",
                "color": "red"
            },
            "proxy_needed": {
                "message": "Proxy needed..",
                "group": "Accurate Edit Module",
                "icon": "fa-thin fa-video-slash",
                "color": "grey"
            },
            "type": {
                "message": "Detected: {audioConfig}",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-waveform-lines",
                "color": "#2196F3"
            },
            "proxy_start": {
                "message": "Proxy conversion started..",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-shuffle",
                "color": "#2196F3"
            },
            "proxy_complete": {
                "message": "Proxy complete",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-shuffle",
                "color": "green"
            },
            "proxy_missing": {
                "message": "Proxy Missing after conversion",
                "group": "Accurate Edit Module",
                "icon": "fa-thin fa-video-slash",
                "color": "red"
            },
            "edl_prep": {
                "message": "Preparing edl",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-arrow-progress",
                "color": "#2196F3"
            },
            "active_wo": {
                "message": "Pending WO",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-person-chalkboard",
                "color": "#2196F3"
            },
            "complete_wo": {
                "message": "Completed WO",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-person-chalkboard",
                "color": "green"
            },
            "missing_edl": {
                "message": "Access EDL missing",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-file-slash",
                "color": "red"
            },
            "render_start": {
                "message": "Rendering in progress..",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-shuffle",
                "color": "#2196F3"
            },
            "render_complete": {
                "message": "Render complete",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-shuffle",
                "color": "green"
            },
            "render_fail": {
                "message": "Render failed",
                "group": "Accurate Edit Module",
                "icon": "fa-duotone fa-shuffle",
                "color": "red"
            },
            "missing_render": {
                "message": "Access render missing",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-file-slash",
                "color": "red"
            },
            "complete": {
                "message": "Edit Complete",
                "group": "Accurate Edit Module",
                "icon": "fa-solid fa-ballot-check",
                "color": "green"
            }
        },
        "transitions": {
            "on_init": [
                {
                    "operation": "clear",
                    "groups": ["Accurate Edit Module"]
                }
            ],
            "on_start": [
                {
                    "operation": "add",
                    "keys": ["start"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["start"]
                }
            ],
            "on_too_many_primary": [
                {
                    "operation": "delete",
                    "keys": ["start"]
                },
                {
                    "operation": "add",
                    "keys": ["too_many_primary"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["too_many_primary"]
                }
            ],
            "on_missing_file": [
                {
                    "operation": "delete",
                    "keys": ["start"]
                },
                {
                    "operation": "add",
                    "keys": ["missing_file"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["missing_file"]
                }
            ],
            "on_proxy_needed": [
                {
                    "operation": "add",
                    "keys": ["proxy_needed"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["proxy_needed"]
                }
            ],
            "on_audio_config": [
                {
                    "operation": "add",
                    "keys": ["type"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["type"]
                }
            ],
            "on_proxy_start": [
                {
                    "operation": "add",
                    "keys": ["proxy_start"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["proxy_start"]
                }
            ],
            "on_proxy_complete": [
                {
                    "operation": "delete",
                    "keys": ["proxy_needed", "proxy_start", "type"]
                },
                {
                    "operation": "add",
                    "keys": ["proxy_complete"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["proxy_complete"]
                }
            ],
            "on_proxy_missing": [
                {
                    "operation": "delete",
                    "keys": ["proxy_complete"]
                },
                {
                    "operation": "add",
                    "keys": ["proxy_missing"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["proxy_missing"]
                }
            ],
            "on_edl_prep": [
                {
                    "operation": "delete",
                    "keys": ["proxy_complete", "proxy_missing"]
                },
                {
                    "operation": "add",
                    "keys": ["edl_prep"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["edl_prep"]
                }
            ],
            "on_active_wo": [
                {
                    "operation": "delete",
                    "keys": ["edl_prep"]
                },
                {
                    "operation": "add",
                    "keys": ["active_wo"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["active_wo"]
                }
            ],
            "on_complete_wo": [
                {
                    "operation": "delete",
                    "keys": ["active_wo"]
                },
                {
                    "operation": "add",
                    "keys": ["complete_wo"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["complete_wo"]
                }
            ],
            "on_edl_not_found": [
                {
                    "operation": "delete",
                    "keys": ["complete_wo"]
                },
                {
                    "operation": "add",
                    "keys": ["missing_edl"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["missing_edl"]
                }
            ],
            "on_render_start": [
                {
                    "operation": "delete",
                    "keys": ["complete_wo"]
                },
                {
                    "operation": "add",
                    "keys": ["render_start"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["render_start"]
                }
            ],
            "on_render_complete": [
                {
                    "operation": "delete",
                    "keys": ["render_start"]
                },
                {
                    "operation": "add",
                    "keys": ["render_complete"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["render_complete"]
                }
            ],
            "on_missing_render": [
                {
                    "operation": "delete",
                    "keys": ["render_complete"]
                },
                {
                    "operation": "add",
                    "keys": ["missing_render"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["missing_render"]
                }
            ],
            "on_complete": [
                {
                    "operation": "clear",
                    "groups": ["Accurate Edit Module"]
                },
                {
                    "operation": "add",
                    "keys": ["complete"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["complete"]
                }
            ]
        }
    }
}
