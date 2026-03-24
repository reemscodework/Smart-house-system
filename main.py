import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


class SmartDevice:
    def __init__(self, name):
        self._name = name
        self._switched_on = False

    def toggle_switch(self):
        self._switched_on = not self._switched_on

    def __str__(self):
        state = "on" if self._switched_on else "off"
        return f"{self._name} is {state}"


class SmartTV(SmartDevice):
    def __init__(self, channel=1):
        super().__init__("SmartTV")
        self.channel = channel

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if not (1 <= value <= 734):
            raise ValueError("Channel must be between 1 and 734.")
        self._channel = value

    def __str__(self):
        state = "on" if self._switched_on else "off"
        return f"{self._name} is {state} on channel {self._channel}"


class SmartOven(SmartDevice):
    def __init__(self, temperature=150):
        super().__init__("SmartOven")
        self.temperature = temperature

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not (0 <= value <= 260):
            raise ValueError("Temperature must be between 0 and 260.")
        self._temperature = value

    def __str__(self):
        state = "on" if self._switched_on else "off"
        return f"{self._name} is {state} with a temperature of {self._temperature}°C"


class SmartPlug(SmartDevice):
    def __init__(self, consumption_rate):
        super().__init__("SmartPlug")
        if not (0 <= consumption_rate <= 150):
            raise ValueError("Consumption rate must be between 0 and 150.")
        self._consumption_rate = consumption_rate

    def __str__(self):
        state = "on" if self._switched_on else "off"
        return f"{self._name} is {state} with a consumption rate of {self._consumption_rate}W"

    @property
    def consumption_rate(self):
        return self._consumption_rate

    @consumption_rate.setter
    def consumption_rate(self, value):
        if not (0 <= value <= 150):
            raise ValueError("Consumption rate must be between 0 and 150.")
        self._consumption_rate = value


class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Control Panel")
        self.devices = [
            SmartTV(1),
            SmartOven(150),
            SmartPlug(60)
        ]

        #control buttons need to work
        tk.Button(root, text="Turn on all", command=self.turn_on_all).grid(row=0, column=0, columnspan=1, pady=5)
        tk.Button(root, text="Turn off all", command=self.turn_off_all).grid(row=0, column=2, columnspan=2, pady=5)

        # the devices
        self.device_frames = []
        self.render_devices()

        # Add fix the distant
        tk.Button(root, text="Add", command=self.add_device).grid(row=len(self.devices) + 2, column=0, columnspan=1, pady=5)

    def render_devices(self):
        for frame in self.device_frames:
            frame.destroy()

        self.device_frames = []

        for i, device in enumerate(self.devices):
            label = tk.Label(self.root, text=str(device), anchor="w")
            label.grid(row=i + 1, column=0, columnspan=2, sticky="w", padx=5)
            self.device_frames.append(label)

            tk.Button(self.root, text="Toggle", command=lambda i=i: self.toggle_device(i)).grid(row=i + 1, column=2)
            tk.Button(self.root, text="Edit", command=lambda i=i: self.edit_device(i)).grid(row=i + 1, column=3)
            tk.Button(self.root, text="Delete", command=lambda i=i: self.delete_device(i)).grid(row=i + 1, column=4)

    def toggle_device(self, index):
        self.devices[index].toggle_switch()
        self.render_devices()

    def edit_device(self, index):
        device = self.devices[index]
        try:
            if isinstance(device, SmartTV):
                new_value = simpledialog.askinteger("Edit TV", "Enter new channel (1-734):", minvalue=1, maxvalue=734)
                if new_value is not None:
                    device.channel = new_value
            elif isinstance(device, SmartOven):
                new_value = simpledialog.askinteger("Edit Oven", "Enter new temperature (0-260°C):", minvalue=0, maxvalue=260)
                if new_value is not None:
                    device.temperature = new_value
            elif isinstance(device, SmartPlug):
                new_value = simpledialog.askinteger("Edit Plug", "Enter new consumption rate (0-150W):", minvalue=0, maxvalue=150)
                if new_value is not None:
                    device.consumption_rate = new_value
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

        self.render_devices()

    def delete_device(self, index):
        del self.devices[index]
        self.render_devices()

    def turn_on_all(self):
        for device in self.devices:
            device._switched_on = True
        self.render_devices()

    def turn_off_all(self):
        for device in self.devices:
            device._switched_on = False
        self.render_devices()

    def add_device(self):
        device_type = simpledialog.askstring("Add Device", "Enter device type (SmartTV, SmartOven, SmartPlug):")
        try:
            if device_type == "SmartTV":
                self.devices.append(SmartTV())
            elif device_type == "SmartOven":
                self.devices.append(SmartOven())
            elif device_type == "SmartPlug":
                consumption = simpledialog.askinteger("Add SmartPlug", "Enter consumption rate (0-150W):", minvalue=0, maxvalue=150)
                self.devices.append(SmartPlug(consumption))
            else:
                messagebox.showerror("Error", "Invalid device type")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        self.render_devices()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
