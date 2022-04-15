# Главный файл программы, использующий вс остальные функции

from const import *  # здесь находятся все коды, их не выкладываем на гит хаб, передаем в дискорде
import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
