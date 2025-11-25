// Auto-generated from discoveries.json
// Generated: 2025-11-25T02:57:57.045463Z

const discoveries = [
  {
    "repository": {
      "owner": "kubernetes-sigs",
      "name": "kubespray",
      "url": "https://github.com/kubernetes-sigs/kubespray",
      "stars": 17951,
      "language": "Jinja"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/kubernetes-sigs/kubespray/blob/master/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 10,
      "reasoning": "High-quality peer: CI/CD via .gitlab-ci.yml; tests in tests/; active (0d ago); 376 contributors; 28 related repos"
    },
    "contacts": [
      {
        "type": "github",
        "value": "gregbkr",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "rsmitty",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "pamelafox",
      "name": "python-project-template",
      "url": "https://github.com/pamelafox/python-project-template",
      "stars": 146,
      "language": "Python"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/pamelafox/python-project-template/blob/main/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 8,
      "reasoning": "High-quality peer: tests in tests/; devcontainer setup; active (0d ago); 4 contributors; 5 related repos"
    },
    "contacts": [
      {
        "type": "github",
        "value": "pamelafox",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "Kong",
      "name": "kong",
      "url": "https://github.com/Kong/kong",
      "stars": 42255,
      "language": "Lua"
    },
    "discovery": {
      "markdown_file": "DEVELOPER.md",
      "file_url": "https://github.com/Kong/kong/blob/master/DEVELOPER.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 8,
      "reasoning": "High-quality peer: tests in spec/; devcontainer setup; active (10d ago); 338 contributors; 18 related repos"
    },
    "contacts": [
      {
        "type": "email",
        "value": "security@konghq.com",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "github",
        "value": "konghq",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "email",
        "value": "support@konghq.com",
        "source_file": "CODE_OF_CONDUCT.md",
        "confidence": "high"
      }
    ]
  },
  {
    "repository": {
      "owner": "k3s-io",
      "name": "k3s",
      "url": "https://github.com/k3s-io/k3s",
      "stars": 31394,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/k3s-io/k3s/blob/main/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 6,
      "reasoning": "Medium-quality: tests in tests/; active (0d ago); 266 contributors; 1 related repos"
    },
    "contacts": [
      {
        "type": "email",
        "value": "security@k3s.io",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "k3s",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "ahmetb",
      "name": "kubectx",
      "url": "https://github.com/ahmetb/kubectx",
      "stars": 19234,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/ahmetb/kubectx/blob/master/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 6,
      "reasoning": "Medium-quality: tests in test/; 63 contributors; 4 related repos"
    },
    "contacts": [
      {
        "type": "github",
        "value": "ahmetb",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "derailed",
      "name": "k9s",
      "url": "https://github.com/derailed/k9s",
      "stars": 31925,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/derailed/k9s/blob/master/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 5,
      "reasoning": "Medium-quality: CI/CD via .travis.yml; active (0d ago); 334 contributors"
    },
    "contacts": [
      {
        "type": "email",
        "value": "fernand@imhotep.io",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "kitesurfer",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "imhotep",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "goharbor",
      "name": "harbor",
      "url": "https://github.com/goharbor/harbor",
      "stars": 26942,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/goharbor/harbor/blob/main/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 5,
      "reasoning": "Medium-quality: tests in tests/; active (0d ago); 329 contributors; 1 related repos"
    },
    "contacts": [
      {
        "type": "email",
        "value": "cncf-harbor-security@lists.cncf.io",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "email",
        "value": "cncf-harbor-distributors-announce@lists.cncf.io",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "github",
        "value": "lists",
        "source_file": "SECURITY.md",
        "confidence": "high"
      }
    ]
  },
  {
    "repository": {
      "owner": "jina-ai",
      "name": "serve",
      "url": "https://github.com/jina-ai/serve",
      "stars": 21796,
      "language": "Python"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/jina-ai/serve/blob/master/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 5,
      "reasoning": "Medium-quality: tests in tests/; 161 contributors; 2 related repos"
    },
    "contacts": [
      {
        "type": "email",
        "value": "security@jina.ai",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "github",
        "value": "jina",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "github",
        "value": "requests",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "vitessio",
      "name": "vitess",
      "url": "https://github.com/vitessio/vitess",
      "stars": 20491,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "CLAUDE.md",
      "file_url": "https://github.com/vitessio/vitess/blob/main/CLAUDE.md",
      "patterns_found": [
        "git log"
      ]
    },
    "quality": {
      "score": 5,
      "reasoning": "Medium-quality: tests in test/; active (0d ago); 321 contributors"
    },
    "contacts": [
      {
        "type": "email",
        "value": "cncf-vitess-maintainers@lists.cncf.io",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "github",
        "value": "lists",
        "source_file": "SECURITY.md",
        "confidence": "high"
      }
    ]
  },
  {
    "repository": {
      "owner": "GoogleCloudPlatform",
      "name": "microservices-demo",
      "url": "https://github.com/GoogleCloudPlatform/microservices-demo",
      "stars": 19378,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/GoogleCloudPlatform/microservices-demo/blob/main/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 5,
      "reasoning": "Medium-quality: active (0d ago); 128 contributors; 51 related repos"
    },
    "contacts": [
      {
        "type": "github",
        "value": "GoogleCloudPlatform",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "xtruder",
      "name": "nix-devcontainer",
      "url": "https://github.com/xtruder/nix-devcontainer",
      "stars": 300,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/xtruder/nix-devcontainer/blob/main/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 4,
      "reasoning": "Low production signals: tests in test/; devcontainer setup; 4 contributors"
    },
    "contacts": [
      {
        "type": "email",
        "value": "jaka@x-truder.net",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "Rizary",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "offlinehacker",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "johannes-mueller",
      "name": "devcontainer.el",
      "url": "https://github.com/johannes-mueller/devcontainer.el",
      "stars": 69,
      "language": "Emacs Lisp"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/johannes-mueller/devcontainer.el/blob/master/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 4,
      "reasoning": "Low production signals: tests in test/; 4 contributors; 1 related repos"
    },
    "contacts": [
      {
        "type": "github",
        "value": "devcontainers",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "felipecrs",
      "name": "docker-images",
      "url": "https://github.com/felipecrs/docker-images",
      "stars": 40,
      "language": "Shell"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/felipecrs/docker-images/blob/master/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 4,
      "reasoning": "Low production signals: devcontainer setup; active (0d ago); 3 contributors"
    },
    "contacts": [
      {
        "type": "github",
        "value": "felipecrs",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "containers",
      "name": "podman",
      "url": "https://github.com/containers/podman",
      "stars": 29784,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/containers/podman/blob/main/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 4,
      "reasoning": "Low production signals: tests in test/; active (0d ago); 422 contributors"
    },
    "contacts": [
      {
        "type": "email",
        "value": "podman-join@lists.podman.io",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "email",
        "value": "security@lists.podman.io",
        "source_file": "README.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "lists",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "verdaccio",
      "name": "verdaccio",
      "url": "https://github.com/verdaccio/verdaccio",
      "stars": 17286,
      "language": "TypeScript"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/verdaccio/verdaccio/blob/master/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 4,
      "reasoning": "Low production signals: active (1d ago); 278 contributors; 1 related repos"
    },
    "contacts": [
      {
        "type": "email",
        "value": "publickey.verdaccio@pm.me.asc",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "email",
        "value": "verdaccio@pm.me",
        "source_file": "SECURITY.md",
        "confidence": "high"
      },
      {
        "type": "github",
        "value": "pm",
        "source_file": "SECURITY.md",
        "confidence": "high"
      }
    ]
  },
  {
    "repository": {
      "owner": "qdm12",
      "name": "godevcontainer",
      "url": "https://github.com/qdm12/godevcontainer",
      "stars": 280,
      "language": "Dockerfile"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/qdm12/godevcontainer/blob/master/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 3,
      "reasoning": "Low production signals: devcontainer setup; active (4d ago); 3 contributors"
    },
    "contacts": [
      {
        "type": "github",
        "value": "qdm12",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "eip-work",
      "name": "kuboard-press",
      "url": "https://github.com/eip-work/kuboard-press",
      "stars": 24551,
      "language": "JavaScript"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/eip-work/kuboard-press/blob/master/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 3,
      "reasoning": "Low production signals: devcontainer setup; 15 contributors"
    },
    "contacts": [
      {
        "type": "github",
        "value": "eip-work",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "devrt",
      "name": "ros-devcontainer-vscode",
      "url": "https://github.com/devrt/ros-devcontainer-vscode",
      "stars": 202,
      "language": "Dockerfile"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/devrt/ros-devcontainer-vscode/blob/master/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 2,
      "reasoning": "Low production signals: devcontainer setup"
    },
    "contacts": [
      {
        "type": "github",
        "value": "devrt",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "ContainerCraft",
      "name": "devcontainer",
      "url": "https://github.com/ContainerCraft/devcontainer",
      "stars": 43,
      "language": "Dockerfile"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/ContainerCraft/devcontainer/blob/main/README.md",
      "patterns_found": [
        "kubectl",
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 2,
      "reasoning": "Low production signals: devcontainer setup; rich discovery patterns (score: 11)"
    },
    "contacts": [
      {
        "type": "github",
        "value": "ContainerCraft",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "helm",
      "name": "helm",
      "url": "https://github.com/helm/helm",
      "stars": 29085,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "CONTRIBUTING.md",
      "file_url": "https://github.com/helm/helm/blob/main/CONTRIBUTING.md",
      "patterns_found": [
        "git log"
      ]
    },
    "quality": {
      "score": 2,
      "reasoning": "Low production signals: active (0d ago); 372 contributors"
    },
    "contacts": [
      {
        "type": "email",
        "value": "cncf-helm-security@lists.cncf.io",
        "source_file": "CONTRIBUTING.md",
        "confidence": "low"
      },
      {
        "type": "email",
        "value": "cncf-helm@lists.cncf.io",
        "source_file": "CONTRIBUTING.md",
        "confidence": "low"
      },
      {
        "type": "github",
        "value": "lists",
        "source_file": "CONTRIBUTING.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "openfaas",
      "name": "faas",
      "url": "https://github.com/openfaas/faas",
      "stars": 25986,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "CONTRIBUTING.md",
      "file_url": "https://github.com/openfaas/faas/blob/master/CONTRIBUTING.md",
      "patterns_found": [
        "kubectl",
        "docker (ps|images|logs)",
        "git log"
      ]
    },
    "quality": {
      "score": 2,
      "reasoning": "Low production signals: active (23d ago); 161 contributors"
    },
    "contacts": [
      {
        "type": "email",
        "value": "joe.smith@email.com",
        "source_file": "CONTRIBUTING.md",
        "confidence": "low"
      },
      {
        "type": "email",
        "value": "sales@openfaas.com",
        "source_file": "CONTRIBUTING.md",
        "confidence": "low"
      },
      {
        "type": "email",
        "value": "support@openfaas.com",
        "source_file": "CONTRIBUTING.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "abiosoft",
      "name": "colima",
      "url": "https://github.com/abiosoft/colima",
      "stars": 25640,
      "language": "Go"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/abiosoft/colima/blob/main/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 2,
      "reasoning": "Low production signals: active (0d ago); 91 contributors"
    },
    "contacts": [
      {
        "type": "github",
        "value": "abiosoft",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "mamba-org",
      "name": "micromamba-devcontainer",
      "url": "https://github.com/mamba-org/micromamba-devcontainer",
      "stars": 40,
      "language": "Shell"
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/mamba-org/micromamba-devcontainer/blob/main/README.md",
      "patterns_found": [
        "docker (ps|images|logs)"
      ]
    },
    "quality": {
      "score": 1,
      "reasoning": "Low production signals: 2 contributors"
    },
    "contacts": [
      {
        "type": "github",
        "value": "devcontainer",
        "source_file": "README.md",
        "confidence": "low"
      }
    ]
  },
  {
    "repository": {
      "owner": "milanm",
      "name": "DevOps-Roadmap",
      "url": "https://github.com/milanm/DevOps-Roadmap",
      "stars": 17800,
      "language": null
    },
    "discovery": {
      "markdown_file": "README.md",
      "file_url": "https://github.com/milanm/DevOps-Roadmap/blob/master/README.md",
      "patterns_found": [
        "kubectl"
      ]
    },
    "quality": {
      "score": 1,
      "reasoning": "Low production signals: 12 contributors"
    },
    "contacts": [
      {
        "type": "github",
        "value": "milanm",
        "source_file": "repository_owner",
        "confidence": "low"
      }
    ]
  }
];
