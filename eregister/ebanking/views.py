from django.shortcuts import render
from ebanking.forms import RegistrationForm
from django.views import View
from datetime import datetime
import psycopg2 as psql
from django.contrib import messages
import urllib.parse
from django.shortcuts import redirect
from ebanking.configs import EXECUTION_MODE
from ebanking.configs import ALLOWED_CHANNELS
from ebanking.configs import SALT_CODE
from ebanking.utils import generate_sha256
from ebanking.email_utils import shoot_email
from ebanking.configs import DB_USERNAME
from ebanking.configs import DB_PASSWORD
from ebanking.configs import DB_HOST
from ebanking.configs import DB_PORT
from ebanking.configs import DB_NAME
from ebanking.configs import TB_NAME_CARD_HASH
from ebanking.configs import TB_NAME_AUTH_REQUESTS
from ebanking.utils import decode_base64
import threading
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ebanking.email_utils import shoot_csp_violation_email
import json


def save_auth_request(
                    rim, auth_status, auth_desc,
                    channel, session_id, phone, cursor, psqldb
                    ):
    sql = ("INSERT INTO " + TB_NAME_AUTH_REQUESTS + "(rim, created_date," +
           "auth_status, auth_des, channel, session_id, phone)" +
           " VALUES (%s, %s, %s, %s, %s, %s, %s)")

    data = (rim, datetime.now(), auth_status, auth_desc,
            channel, session_id, phone)
    cursor.execute(sql, data)
    psqldb.commit()


def close_db(cursor, psqlDB):
    if cursor:
        cursor.close()

    if psqlDB:
        psqlDB.close()


def clear_form(form):
    return RegistrationForm()


class RegistrationView(View):
    AUTH_STATUS_SUCCESS = "0"
    AUTH_STATUS_INVALID_CPR = "1"
    AUTH_STATUS_INVALID_DOB = "2"
    AUTH_STATUS_INVALID_CARD_OR_EXPIRY = "3"
    AUTH_STATUS_INVALID_CHANNEL = "4"
    AUTH_SUCCESS_MESSAGE = ('Your authentication is success.' +
                            ' Your account will be activated within one' +
                            ' hour, else our customer care executive will' +
                            ' call you to complete the' +
                            ' registration process.')

    def get(self, request):
        print("In GET request : " + str(request))
        referer_channel_url = None
        print("Referrer url : " + str(request))
        print("Referrer server : " + str(request.GET.get('callback_url')))
        try:
            callback_url = request.GET.get('callback_url', None)
            referer_channel_url = str(callback_url)
        except Exception as e:
            print("Exception", e)

        print("Referrer channel url : " + str(referer_channel_url))

        if (EXECUTION_MODE == 1 and not referer_channel_url):
            return render(request, 'blank.html')

        if (EXECUTION_MODE == 0 and referer_channel_url):
            return render(request, 'blank.html')

        channel_name = None
        for key in ALLOWED_CHANNELS.keys():
            if referer_channel_url == ALLOWED_CHANNELS[key]:
                channel_name = key
                break

        print("Found matching channel name : " + str(channel_name))

        if EXECUTION_MODE == 0 or channel_name:
            return render(
                        request,
                        'index.html',
                        {'form': RegistrationForm(), 'channel': channel_name}
                        )
        else:
            try:
                if channel_name:
                    return redirect(str(referer_channel_url), permanent=True)
                else:
                    return render(request, 'blank.html')
            except Exception as e:
                return render(
                            request,
                            'index.html',
                            {'form': RegistrationForm(),
                             'channel': channel_name}
                            )

    def post(self, request):
        callback_url = request.GET.get('callback_url', None)
        session_id = request.GET.get('session_id', None)

        if callback_url and session_id:
            callback_url = urllib.parse.unquote_plus(callback_url)
            session_id = urllib.parse.unquote_plus(session_id)

        print("POST : callback_url = "+str(callback_url))
        print("POST : session_id = " + str(session_id))

        form = RegistrationForm(request.POST)

        if form.data['channel']:
            channel = form.data['channel']
        else:
            channel = 'Standalone'

        if form.is_valid():
            print("Form is validated")

            rim = card_hash = phone = None

            cpr = form.cleaned_data.get("cpr")
            card_number = form.cleaned_data.get("card_number")
            expiry = form.cleaned_data.get("expiry")
            dob = form.cleaned_data.get("dob")

            hash_input = card_number + expiry + SALT_CODE
            hash_output = generate_sha256(hash_input)
            #print("hash_input = "+hash_input)
            print("hash_output = "+hash_output)

            psqlDB = cursor = None
            try:
                psqlDB = psql.connect(user=DB_USERNAME,
                                      password=decode_base64(DB_PASSWORD),
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)

                cursor = psqlDB.cursor()
                cursor.execute(("SELECT * FROM " + TB_NAME_CARD_HASH +
                                " WHERE card_exp_hash = '" +
                                hash_output + "'"))
                card_hash = cursor.fetchall()

                if len(card_hash) == 0:
                    print("HashToken is NOT found in table")
                    cursor.execute(("SELECT * FROM " + TB_NAME_CARD_HASH +
                                    " WHERE cpr = '" + cpr + "' limit 1"))
                    card_hash_by_cpr = cursor.fetchall()
                    if len(card_hash_by_cpr) == 1:
                        rim = card_hash_by_cpr[0][4]
                        phone = card_hash_by_cpr[0][6]

                    save_auth_request(rim,
                                      self.AUTH_STATUS_INVALID_CARD_OR_EXPIRY,
                                      "Invalid Card or Expiry",
                                      channel, session_id, phone,
                                      cursor, psqlDB)
                    form = clear_form(form)
                    form.add_error(None, "Invalid Card or Expiry")
                    return render(
                                request,
                                'index.html',
                                {'form': form, 'channel': channel})
                else:
                    print("HashToken is found in table")

                    card_hash_cpr = card_hash[0][2]
                    card_hash_rim = card_hash[0][4]
                    card_hash_dob = card_hash[0][5]
                    card_hash_phn = card_hash[0][6]
                    card_hash_account_number = card_hash[0][1]

                    if card_hash_cpr != cpr:
                        form = clear_form(form)
                        form.add_error(None, "Invalid CPR")
                        save_auth_request(card_hash_rim,
                                          self.AUTH_STATUS_INVALID_CPR,
                                          "Invalid CPR", channel, session_id,
                                          card_hash_phn, cursor, psqlDB)

                        return render(request,
                                      'index.html',
                                      {'form': form, 'channel': channel})

                    if card_hash_dob != dob:
                        form = clear_form(form)
                        form.add_error(None, "Invalid Date of birth")
                        save_auth_request(card_hash_rim,
                                          self.AUTH_STATUS_INVALID_DOB,
                                          "Invalid Date of birth", channel,
                                          session_id, card_hash_phn, cursor,
                                          psqlDB)

                        return render(request,
                                      'index.html',
                                      {'form': form, 'channel': channel})

                    save_auth_request(card_hash_rim, self.AUTH_STATUS_SUCCESS,
                                      "Success", channel, session_id,
                                      card_hash_phn, cursor, psqlDB)
                    close_db(cursor, psqlDB)

                    if EXECUTION_MODE == 0:
                        messages.success(request, self.AUTH_SUCCESS_MESSAGE)
                        args_tpl = (card_hash_account_number,
                                    card_hash_cpr,
                                    card_hash_rim, channel,
                                    card_hash_phn if card_hash_phn else 'NA',)
                        threading.Thread(target=shoot_email,
                                         args=args_tpl).start()
                        form = RegistrationForm()
                        return render(
                                    request,
                                    'index.html',
                                    {'form': form, 'channel': channel}
                                    )
                    elif EXECUTION_MODE == 1:
                        msg = 'Authentication is success.'
                        auth_status = self.AUTH_STATUS_SUCCESS
                        return render(request, 'index.html',
                                      {'form': RegistrationForm(),
                                       'session_id': session_id,
                                       'callback_url': callback_url,
                                       'auth_status_code': auth_status,
                                       'auth_status_description': msg,
                                       'rim_no': card_hash_rim,
                                       'channel': channel})
                    else:
                        print("Invalid execution mode is found")
            except Exception as e:
                print(e)
                close_db(cursor, psqlDB)
                return render(
                            request,
                            'index.html',
                            {'form': form, 'channel': channel}
                            )
        else:
            print("Form is not validated")
            return render(
                        request,
                        "index.html",
                        {"form": form, 'channel': channel}
                        )


@method_decorator(csrf_exempt, name='dispatch')
class CSPViolationView(View):

    def post(self, request):
        try:
            violation_data = str(request.body.decode("utf-8"))
            violation_json_obj = json.loads(violation_data)
            server_domain = request.META['HTTP_HOST']
            args_tpl = (server_domain, json.dumps(violation_json_obj))
            threading.Thread(target=shoot_csp_violation_email,
                             args=args_tpl).start()
        except Exception as e:
            print(e)
        return redirect("/eregister/", permanent=True)
