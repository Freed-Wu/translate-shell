# GUI

Now this program support GUI in Linux, Android, macOS and Windows.

Need [py-notifier](https://pypi.org/project/py-notifier) to be installed.

## GNU/Linux

Need [libnotify](https://gitlab.gnome.org/GNOME/libnotify) to be installed.

Provide a desktop entry:

![desktop entry](https://user-images.githubusercontent.com/32936898/205704540-cf985b68-4b2f-4095-a5db-88982c809a04.jpg)

Use mouse to select a region of text then the selection buffer will change,
the translation of the text will occur in a notification.

![GNU/Linux](https://user-images.githubusercontent.com/32936898/205699484-c6fdefd5-dca2-4263-aed4-e41d9d16fde6.jpg)

You can customize the notification position in the control center of your
desktop environment.

![control center](https://user-images.githubusercontent.com/32936898/206079338-56428a9c-c840-4de6-a6b0-36ae9764a475.jpg)

## Android

Need [Termux-API](https://github.com/termux/termux-api) to be installed.

If you install [Termux-Widget](https://github.com/termux/termux-widget), you
can get a desktop widget by create
`/data/data/com.termux/files/home/.shortcuts/trans` and refresh:

```sh
trans
```

Press the button, then go to any page.

![android-widget](https://user-images.githubusercontent.com/32936898/206078652-cdee96bb-6ef6-4dc4-af6c-7d619e08a8a0.jpg)

Copy a region of text then the clipboard content will change,
the result will be displayed in a toast and notification.

![android-copy](https://user-images.githubusercontent.com/32936898/206078635-4115454a-2d1a-4e55-ba5b-0916e6023fcb.jpg)

![android-toast](https://user-images.githubusercontent.com/32936898/206078648-0db6480f-7e35-4252-9f33-9fb51e03e172.jpg)

![android-notification](https://user-images.githubusercontent.com/32936898/206078643-a0fb7f94-01f5-4b98-b93f-f4b80c2abde6.jpg)

## macOS

Need [pync](https://github.com/SeTeM/pync) to be installed.

Use mouse to select a region of text then the selection buffer will change,
the translation of the text will occur in a notification.

## Windows

Need
[win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications) to
be installed.

Copy a region of text then the clipboard content will change,
the translation of the text will occur in a toast.
