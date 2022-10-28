from stages.stage import Stage
from stages.main_menu import MainMenu
from stages.stage_testing import StageTesting

main_menu:Stage = MainMenu()
stage_testing:Stage = StageTesting()

active_stage:Stage = main_menu