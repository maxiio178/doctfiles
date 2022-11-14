import psutil
import os
import subprocess
from libqtile import hook
from typing import List
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

#----   Variables 1  ------
dispositivo_red = 'enp2s0'
mod = "mod4"
terminal = guess_terminal()
color_barra="#2F2827"
tamano_barra=20
fuente_predeterminada="Hack"
tamano_fuente=14
color_active="#6f65d4" # Amarillento
color_fg= "#FF4A00" # 
color_bg= "#2F2827" #
color_inactive= '#A9EADF' # azulito
color_claro = '#BD93F9' #
color_urgent = '#FF5555' #
color_oscuro = '#44475A' #
color_texto1= '#729289' #
tamanos_iconos = 18
color_etiqueta1 = "#6f65d4" #narajadito #'#158457' #verde #'
color_etiqueta2 = '#4F2B7A'# moradito #'#158457' #verde #'
color_etiqueta3 = '#5090B0'# azuloso #'#158457' #verde #'
color_etiqueta4 = '#6D2441'# lila oscuro #'#158457' #verde #'
color_iconos= '#A9EADF'  # claro

#------ Funciones creadas 1 ------
def fc_separador():
    return  widget.Sep(
            linewidth = 0,
            foreground = color_fg,
            background = color_bg,
            padding = 3,
         )
def fc_etiqueta(vColor,tipo):
    if tipo == 0:
        icono = ''
    else:
        icono = ''
    return widget.TextBox(
        text = icono,
        fontsize = 23,
        foreground= vColor,
        background = color_bg,
        padding=0.9,
    )
def fc_icono(icono, color_etiqueta):
    return widget.TextBox(
        text= icono,
        foreground= color_iconos,
        background= color_etiqueta,
        fontsize = 15,
    )

# ----- Atajos de teclado -------
keys = [
    #-Move focus to-
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),
    #-Move window to the-
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()), 
    #-window to the-
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    #-Volumen por teclado-
    Key([mod], "o", lazy.spawn('pactl set-sink-volume 0 -3%')),
    Key([mod], "i", lazy.spawn('pactl set-sink-volume 0 +3%')),
    Key([mod], 'p', lazy.spawn('pactl set-sink-mute 0 toggle')),
    #---Vrillo pantalla----
    Key([mod], "z", lazy.spawn('brightnessctl set +10%')),
    Key([mod], "x", lazy.spawn('brightnessctl set -10%')),
    # -- capturar pantalla --
    Key([mod], "f", lazy.spawn('scrot')),
    #-Automatic key-
    Key([mod, "shift"],"Return",lazy.layout.toggle_split()),
    Key([mod], "s", lazy.spawn("spotify")),
    Key([mod], "Return", lazy.spawn("kitty")), 
    Key([mod, "control"], "Return", lazy.spawn("alacritty")),
    Key([mod], "c", lazy.spawn('code')),
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    Key([mod, "control"], "b", lazy.spawn("google-chrome-stable")),
    Key([mod], "b", lazy.spawn("firefox")),
    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]
#---- Iconos -----
groups = [
    Group(i) for i in [
        "ﲤ", "", "", "", "", "", "", "", " ",
        ]]

#----- BARRA DE TAREAS -----
for i, group in enumerate(groups):
    numerosEscritorio=str(i+1)
    keys.extend(
        [Key([mod],numerosEscritorio,lazy.group[group.name].toscreen(),desc="Switch to group {}"
        .format(group.name),),
            Key([mod, "shift"],numerosEscritorio,lazy.window.togroup(group.name, switch_group=True),
            desc="{}".format(group.name)),]
    )

#----- LAYOUTS -----
layouts = [
    layout.Columns(border_focus=color_etiqueta1, border_width=1, margin=3),
    layout.Max(),
]
#----- Widget -----
widget_defaults = dict(
    font=fuente_predeterminada,
    fontsize=tamano_fuente,
    padding=3,
)
extension_defaults = widget_defaults.copy()
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=color_active,
                    border_width= 1,
                    disable_drag= True,
                    fontsize = tamanos_iconos,
                    foreground=color_fg,
                    highlight_method = 'block',
                    inactive = color_inactive,
                    margin_x = 0,
                    margin_y = 5,
                    this_current_screen_border = color_claro,
                    this_screen_border = color_oscuro,
                    urgent_alert_method ='blok',
                    urgent_border = color_urgent,
                ),
                
                widget.WindowName(
                    background = color_bg,
                    foreground = color_texto1,
                ),
                #-Etiqueta temperatura-
                fc_etiqueta(color_etiqueta1, 0),
                
                fc_icono("", color_etiqueta1),
                widget.ThermalSensor(
                    foreground=color_inactive,
                    background=color_etiqueta1,
                    threshold=60,
                    tag_sensor="Core 0",
                    fmt = "{}"
                ),

                fc_icono('', color_etiqueta1),
                widget.Memory(
                    foreground=color_inactive,
                    background=color_etiqueta1,    
                ),

                #-Etiqueta de actualizaciones-
                fc_etiqueta(color_etiqueta2,0),
                fc_icono('', color_etiqueta1),
                widget.CheckUpdates(
                    background = color_etiqueta1,
                    colour_have_updates = color_iconos,
                    color_no_updates = color_texto1,
                    no_update_string = '0',
                    display_format = '{updates}',
                    update_interval =1800,
                    distra ='Arch_checkupdates',
                ),
            

                #-Etiqueta hora-volumen-
                
                fc_icono('', color_etiqueta1),
                widget.Clock(
                    format=" %a %d %m  %I:%M %p",
                    foreground= color_iconos,
                    background= color_etiqueta1,
                    ),

                widget.PulseVolume(
                    foreground = color_iconos,
                    background = color_etiqueta1,
                    limit_max_volume = True,
                    fontsize = tamano_fuente,
                ),

                #etiqueta-max-colum

                fc_icono('', color_etiqueta1),
                widget.CurrentLayout(
                    background= color_etiqueta1,
                    foreground=color_iconos,
                    fmt ='{}',
                    
                ),

            ],
            tamano_barra,
            background=color_barra,
        ),
    ),
]
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wmname = "LG3D"
 
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])