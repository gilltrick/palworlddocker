from flask import Flask, render_template, request, redirect
from palsp.service import runner
from palsp.configurator import configurator
from .sessionHandler import *

webserver = Flask(__name__)
config = None
server_runner = None
palworld_configurator = None
session_handler = None

@webserver.route("/")
def index():
    palworld_server_settings = palworld_configurator.load_config()
    if palworld_server_settings == {}:
        palworld_server_settings = palworld_configurator.load_export_config()
    return render_template("index.html", palworld_server_settings=palworld_server_settings)

@webserver.route("/login", methods=["get"])
def login():
    return render_template("login.html")

@webserver.route("/login", methods=["post"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]
    if username == config["website_user"] and password == config["website_password"]:
        session_handler.remove_session(request)
        session_handler.create_session("0", request, 1800)
    return redirect("/")


@webserver.route("/do")
def do():
    if session_handler.simple_authenticate(request):
        cmd = request.args.get("cmd")
        print("valid user")
        if cmd == "start":
            server_runner.start_server()
        if cmd == "stop":
            server_runner.stop_server()
        if cmd == "restart":
            server_runner.restart_server()
        if cmd == "create_backup":
            server_runner.create_manual_backup()
        if cmd == "applay_backup":
            server_runner.apply_backup_manual()
        if cmd == "update_server":
            server_runner.update_server()
    return redirect("/")

@webserver.route("/updateConfig", methods=["post"])
def update_config():
    if session_handler.simple_authenticate(request):
        x = {
        "Difficulty":request.form["Difficulty"],
        "DayTimeSpeedRate":request.form["DayTimeSpeedRate"],
        "NightTimeSpeedRate":request.form["NightTimeSpeedRate"],
        "ExpRate":request.form["ExpRate"],
        "PalCaptureRate":request.form["PalCaptureRate"],
        "PalSpawnNumRate":request.form["PalSpawnNumRate"],
        "PalDamageRateAttack":request.form["PalDamageRateAttack"],
        "PalDamageRateDefense":request.form["PalDamageRateDefense"],
        "PlayerDamageRateAttack":request.form["PlayerDamageRateAttack"],
        "PlayerDamageRateDefense":request.form["PlayerDamageRateDefense"],
        "PlayerStomachDecreaceRate":request.form["PlayerStomachDecreaceRate"],
        "PlayerStaminaDecreaceRate":request.form["PlayerStaminaDecreaceRate"],
        "PlayerAutoHPRegeneRate":request.form["PlayerAutoHPRegeneRate"],
        "PlayerAutoHpRegeneRateInSleep":request.form["PlayerAutoHpRegeneRateInSleep"],
        "PalStomachDecreaceRate":request.form["PalStomachDecreaceRate"],
        "PalStaminaDecreaceRate":request.form["PalStaminaDecreaceRate"],
        "PalAutoHPRegeneRate":request.form["PalAutoHPRegeneRate"],
        "PalAutoHpRegeneRateInSleep":request.form["PalAutoHpRegeneRateInSleep"],
        "BuildObjectDamageRate":request.form["BuildObjectDamageRate"],
        "BuildObjectDeteriorationDamageRate":request.form["BuildObjectDeteriorationDamageRate"],
        "CollectionDropRate":request.form["CollectionDropRate"],
        "CollectionObjectHpRate":request.form["CollectionObjectHpRate"],
        "CollectionObjectRespawnSpeedRate":request.form["CollectionObjectRespawnSpeedRate"],
        "EnemyDropItemRate":request.form["EnemyDropItemRate"],
        "DeathPenalty":request.form["DeathPenalty"],
        "bEnablePlayerToPlayerDamage":request.form["bEnablePlayerToPlayerDamage"],
        "bEnableFriendlyFire":request.form["bEnableFriendlyFire"],
        "bEnableInvaderEnemy":request.form["bEnableInvaderEnemy"],
        "bActiveUNKO":request.form["bActiveUNKO"],
        "bEnableAimAssistPad":request.form["bEnableAimAssistPad"],
        "bEnableAimAssistKeyboard":request.form["bEnableAimAssistKeyboard"],
        "DropItemMaxNum":request.form["DropItemMaxNum"],
        "DropItemMaxNum_UNKO":request.form["DropItemMaxNum_UNKO"],
        "BaseCampMaxNum":request.form["BaseCampMaxNum"],
        "BaseCampWorkerMaxNum":request.form["BaseCampWorkerMaxNum"],
        "DropItemAliveMaxHours":request.form["DropItemAliveMaxHours"],
        "bAutoResetGuildNoOnlinePlayers":request.form["bAutoResetGuildNoOnlinePlayers"],
        "AutoResetGuildTimeNoOnlinePlayers":request.form["AutoResetGuildTimeNoOnlinePlayers"],
        "GuildPlayerMaxNum":request.form["GuildPlayerMaxNum"],
        "PalEggDefaultHatchingTime":request.form["PalEggDefaultHatchingTime"],
        "WorkSpeedRate":request.form["WorkSpeedRate"],
        "bIsMultiplay":request.form["bIsMultiplay"],
        "bIsPvP":request.form["bIsPvP"],
        "bCanPickupOtherGuildDeathPenaltyDrop":request.form["bCanPickupOtherGuildDeathPenaltyDrop"],
        "bEnableNonLoginPenalty":request.form["bEnableNonLoginPenalty"],
        "bEnableFastTravel":request.form["bEnableFastTravel"],
        "bIsStartLocationSelectByMap":request.form["bIsStartLocationSelectByMap"],
        "bExistPlayerAfterLogout":request.form["bExistPlayerAfterLogout"],
        "bEnableDefenseOtherGuildPlayer":request.form["bEnableDefenseOtherGuildPlayer"],
        "CoopPlayerMaxNum":request.form["CoopPlayerMaxNum"],
        "ServerPlayerMaxNum":request.form["ServerPlayerMaxNum"],
        "ServerName":request.form["ServerName"],
        "ServerDescription":request.form["ServerDescription"],
        "AdminPassword":request.form["AdminPassword"],
        "ServerPassword":request.form["ServerPassword"],
        "PublicPort":request.form["PublicPort"],
        "PublicIP":request.form["PublicIP"],
        "RCONEnabled":request.form["RCONEnabled"],
        "RCONPort":request.form["RCONPort"],
        "Region":request.form["Region"],
        "bUseAuth":request.form["bUseAuth"],
        "BanListURL":request.form["BanListURL"],
    }
        palworld_configurator.save_config(x)
    return redirect("/")

def run(conf=None):
    global config, palworld_configurator, server_runner, session_handler
    config = conf
    palworld_configurator = configurator.Configurator(config)
    server_runner = runner.Runner(palworld_configurator, config)
    session_handler = SessionHandler() 
    webserver.run(debug=True, host=config["hostname"], port=config["website_port"])