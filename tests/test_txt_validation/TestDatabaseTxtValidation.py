from config import ru_txt_path, timezones_txt_path
from tests.response_templates.GeoInfoDataTemplate import GeoInfoDataTemplate
from tests.response_templates.TimezonesDataTemplate import TimezonesDataTemplate


class TestDatabaseTxtValidation:
    def test_ru_txt_validation(self):
        ru = open('../../' + ru_txt_path, 'r', encoding='utf8')
        for string in ru.readlines():
            cells = string.split('\t')
            GeoInfoDataTemplate().check_template_matches(cells)

    def test_timezones_txt_validation(self):
        timezones = open('../../'+timezones_txt_path, 'r', encoding='utf8')
        strings = timezones.readlines()[1:]
        for string in strings:
            cells = string.split('\t')
            TimezonesDataTemplate().check_template_matches(cells)