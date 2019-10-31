from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from psswd.auth import login_required
from psswd.db import get_db


bp = Blueprint('generator', __name__)
