---
tags:
  - nixos
  - capslock
date: 2025-10-24
id: 01K89VE5A80FTXN4AW1RV7FR3B
---
# nixos 修改 capslock 为长按 ctrl 短按 esc

在 `/etc/nixos/configuration` 中这样配置即可：

```nix
services.interception-tools =
  let
    itools = pkgs.interception-tools;
    itools-caps = pkgs.interception-tools-plugins.caps2esc;
  in
  {
    enable = true;
    plugins = [ itools-caps ];
    # requires explicit paths: https://github.com/NixOS/nixpkgs/issues/126681
    udevmonConfig = pkgs.lib.mkDefault ''
      - JOB: "${itools}/bin/intercept -g $DEVNODE | ${itools-caps}/bin/caps2esc -m 1 | ${itools}/bin/uinput -d $DEVNODE"
        DEVICE:
          EVENTS:
            EV_KEY: [KEY_CAPSLOCK, KEY_ESC]
    '';
  };
```

参考连接：https://discourse.nixos.org/t/best-way-to-remap-caps-lock-to-esc-with-wayland/39707/6