from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import markups, CallBackHandler, load_prompt, load_message
import asyncio

