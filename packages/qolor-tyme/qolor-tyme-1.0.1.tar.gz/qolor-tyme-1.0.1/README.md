# Qolor Tyme

This is a Toastmasters-inspired speech timer for use during online daily scrum meeting updates.

![Qolor Tyme screenshot](https://raw.githubusercontent.com/tromgy/qolor-tyme/main/screenshot.png)

It is based on PyQt, which is Python API for Qt (pronounced "cute") cross-platform GUI framework, hence the name Qolor Tyme.

I honestly don't know why they called it PyQt instead of QtPy, which would have made it "cutie-pie" `¯\_(ツ)_/¯`

## Installation

Use **pip**:

```shell
pip install qolor-tyme
```

## Running

Run it as the package. It accepts an optional timeout interval (default is 90 seconds per Agile guidelines)

```shell
python -m qolor_tyme 120
```

This will configure it for 2 minutes timeout. Then, twenty seconds before the timeout the color will change to yellow, five seconds before the timeout it will change to red, and when it times out it will blink red.

The window is set up to be "always on top", so no matter what you (as a scrum master) share on your screen during the meeting, the timer will always be visible.
