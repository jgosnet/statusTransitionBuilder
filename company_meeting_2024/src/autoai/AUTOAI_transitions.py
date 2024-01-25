STATUS_TRANSITIONS = {
    "ai": {
        "statuses": {
            "unsupported_provider": {
                "message": "Unsupported provider ({provider})",
                "group": "AI Module",
                "icon": "fa-solid fa-circle-exclamation",
                "color": "orange"
            },
            "start": {
                "message": "Starting with {provider}",
                "group": "AI Module",
                "icon": "fa-solid fa-play",
                "color": "#2196F3"
            },
            "complete": {
                "message": "complete: {provider}",
                "group": "AI Module",
                "icon": "fa-light fa-brain-circuit",
                "color": "green"
            },
            "failed": {
                "message": "failed: {provider}",
                "group": "AI Module",
                "icon": "fa-light fa-brain-circuit",
                "color": "red"
            },
            "aws": {
                "message": "AWS Rekognition",
                "group": "AI Module",
                "icon": "fa-brands fa-aws",
                "color": "#2196F3"
            },
            "google": {
                "message": "Google Video Intelligence",
                "group": "AI Module",
                "icon": "fa-brands fa-google",
                "color": "#2196F3"
            },
            "azure": {
                "message": "Azure Video indexer",
                "group": "AI Module",
                "icon": "fa-brands fa-windows",
                "color": "#2196F3"
            },
            "proxy_needed": {
                "message": "Proxy needed..",
                "group": "AI Module",
                "icon": "fa-thin fa-video-slash",
                "color": "grey"
            }
        },
        "transitions": {
            "on_start": [
                {
                    "operation": "delete",
                    "keys": ["proxy_needed", "azure", "google", "aws"]
                },
                {
                    "operation": "add",
                    "keys": ["start"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["start"]
                }
            ],
            "on_unsupported_provider": [
                {
                    "operation": "delete",
                    "keys": ["start"]
                },
                {
                    "operation": "add",
                    "keys": ["unsupported_provider"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["unsupported_provider"]
                }
            ],
            "on_aws_rekog": [
                {
                    "operation": "add",
                    "keys": ["aws"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["aws"]
                }
            ],
            "on_google_vi": [
                {
                    "operation": "add",
                    "keys": ["google"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["google"]
                }
            ],
            "on_azure_vi": [
                {
                    "operation": "add",
                    "keys": ["azure"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["azure"]
                }
            ],
            "on_complete": [
                {
                    "operation": "delete",
                    "keys": ["start", "aws", "google", "azure"]
                },
                {
                    "operation": "add",
                    "keys": ["complete"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["complete"]
                }
            ],
            "on_ai_start": [
                {
                    "operation": "delete",
                    "keys": ["proxy_needed"]
                }
            ],
            "on_fail": [
                {
                    "operation": "delete",
                    "keys": ["start"]
                },
                {
                    "operation": "add",
                    "keys": ["fail"]
                },
                {
                    "operation": "add_sc",
                    "keys": ["fail"]
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
            ]
        }
    }
}
