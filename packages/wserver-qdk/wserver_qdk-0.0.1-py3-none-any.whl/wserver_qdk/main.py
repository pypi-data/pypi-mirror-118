""" Модуль содержит основной Singleton для работы. """

from qdk.main import QDK


class WServerQDK(QDK):
    """ Основной класс для взаимодействия с WServer """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_act(self, auto_id, gross, tare, cargo,
                time_in, time_out,
                carrier_id, trash_cat_id, trash_type_id,
                polygon_id, operator, ex_id):
        """
        Добавить новый акт на WServer.

        :param auto_id: ID автомобиля
        :param gross: Вес-брутто
        :param tare: Вес-тара
        :param cargo: Вес-нетто
        :param time_in: Время въезда
        :param time_out: Время выезда
        :param carrier_id: ID перевозчика
        :param trash_cat_id: ID категории груза
        :param trash_type_id: ID вида груза
        :param polygon_id: ID полигона
        :param operator: ID весовщика
        :param ex_id: ID записи в wdb
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_act', auto_id=auto_id, gross=gross, tare=tare,
                            cargo=cargo, time_in=time_in, time_out=time_out,
                            carrier_id=carrier_id, trash_cat_id=trash_cat_id,
                            trash_type_id=trash_type_id, polygon_id=polygon_id,
                            operator=operator, ex_id=ex_id)

    def get_auto_id(self, car_number: str):
        """
        Вернуть ID авто по его гос. номеру.

        :param car_number: гос.номер авто.
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('get_auto_id', car_number=car_number)

    def get_carrier_id(self, carrier_name: str):
        """
        Вернуть ID компании-перевозчика по его названию.

        :param carrier_name: название компании-перевозчика.
        :return:
        """
        self.execute_method('get_company_id', company_name=carrier_name)

    def set_photo(self, record_id: int, photo_obj: str, photo_type: int):
        """
        Сохранить фотографии на WServer.

        :param record_id: ID заезда, к которому относится фотография.
        :param photo_obj: Объект фото в кодировке base64, но в виде строки.
        :param photo_type: Тип фотографии (gdb.photo_types).
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_photos', record=record_id,
                            photo_obj=photo_obj, photo_type=photo_type)

    def set_operator(self, full_name: str, login: str, password: str,
                     polygon: int, active: bool = True):
        """
        Добавить нового весовщика.

        :param full_name: Полное имя весовщика (ФИО).
        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        :param polygon: ID полигона, за которым закреплен весовщик.
        :param active: Запись по умолчанию активна?
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_operator', full_name=full_name, login=login,
                            password=password, polygon=polygon, active=active)

    def set_auto(self, car_number, polygon, id_type, rg_weight=None,
                 model=None, rfid_id=None):
        """
        Добавить новое авто.

        :param car_number: Гос. номер
        :param polygon: Полигон, за которым закреплено авто, если авто
            передвигается по всему региону, его стоит закрепить за РО.
        :param id_type: Протокол авто (rfid, NEG, tails)
        :param rg_weight: Справочный вес (тара)
        :param model: ID модели авто из gdb.auto_models
        :param rfid_id: ID RFID метки из gdb.rfid_marks
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_auto', car_number=car_number, polygon=polygon,
                            id_type=id_type, rg_weight=rg_weight, model=model,
                            rfid_id=rfid_id)

    def set_carrier(self, name, inn, kpp, polygon, status, active, ex_id=None):
        """
         Добавить нового перевозчика.

         :param name: Название перевозчика.
         :param inn: ИНН перевозчика.
         :param kpp: КПП перевозчика.
         :param ex_id: ID перевозичка из внешней системы. (1C, например)
         :param status: Действующий или нет? True/False
         :param polygon: ID полигона.
         :param active: Запись по умолчанию активна?
         :return:
             В случае успеха:
                 {'status': True, 'info': *id: int*)
             В случае провала:
                 {'status': False, 'info': Python Traceback}
         """
        self.execute_method('set_company', name=name, inn=inn, kpp=kpp,
                            polygon=polygon, status=status, ex_id=ex_id,
                            active=active)

    def set_operator_notes(self, record: int, note: str, note_type: int):
        """
        Добавить комментарии весовщика к заезду.

        :param record: ID заезда
        :param note: Комментарий
        :param note_type: Тип комментария (при брутто, добавочный и т.д.)
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_notes', record=record, note=note,
                            note_type=note_type)

    def set_trash_cat(self, name, polygon, active=True):
        """
          Добавить новую категорию груза.

          :param name: Название категории груза.
          :param polygon: ID полигона.
          :param active: Запись по умолчанию активна?
          :return:
              В случае успеха:
                  {'status': True, 'info': *id: int*)
              В случае провала:Отп
                  {'status': False, 'info': Python Traceback}
          """
        self.execute_method('set_trash_cat', name=name, polygon=polygon,
                            active=active)

    def set_trash_type(self, name: str, polygon: int, category: int = None,
                       active: bool = True):
        """
        Добавить новый вид груза.

        :param name: Название вида груза.
        :param category: ID категории груза, за которым этот вид закреплен.
        :param polygon: ID полигона.
        :param active: Запись по умолчанию активна?
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_trash_type', name=name, polygon=polygon,
                            category=category, active=active)

    def get_rfid_id(self, rfid: str):
        """
        Вернуть ID RFID метки по его коду. (10 символов)

        :param rfid: последовательность условной длины, явяляющей частью номера
            RFID метки.
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('get_rfid_id', rfid=rfid)
