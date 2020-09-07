#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import json
from datetime import datetime
import logging
import tornado.web
import tornado.escape

from tornado import gen

from server import webservice
from server.webservice.EndPoints.EndPointRegister import EndPointRegister
from server.webservice.exceptions import Exceptions
from server.webservice.exceptions.Exceptions import InvalidPoolException, SlotRestartException

rf4ce_counter = 0


class MainHandler(tornado.web.RequestHandler):
    """
    Main Handler for tornado web services requests
    """

    # def __init__(self, application, request, **kwargs):
    #     super().__init__(application, request, **kwargs)
    #     self._logger = logging.getLogger()

    def initialize(self):
        try:
            try:
                uuid = self.request.headers
                uuid = uuid["uuid"]
                self._logger = logging.getLogger(uuid)
                self._logger.setLevel(webservice.log_level)
                self._logger.debug("Logger Name: {}".format(self._logger.name))
            except Exception as error:
                self._logger.setLevel(webservice.log_level)
                self._logger.error("Error: {}".format(error))
        except Exceptions as error:
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

    def set_default_headers(self):
        """
        Needed to handle Cross-Origin Resource Sharing
        :return:
        """
        if self.request.headers.get('Origin'):
            self.set_header("Access-Control-Allow-Origin", self.request.headers.get('Origin'))
        else:
            self.set_header("Access-Control-Allow-Origin", 'Origin')
        self.set_header("Connection", self.request.headers.get('Connection'))
        self.set_header("Vary", 'Origin')

    def check_etag_header(self):
        return False

    @gen.coroutine
    def options(self):
        try:
            # Needed to handle Cross-Origin Resource Sharing
            self.set_header("Access-Control-Allow-Headers", "username, uuid, access_token, content-type")
            self.set_header('Access-Control-Allow-Methods', 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT')
            self.set_status(204)
            self.finish()
        except Exceptions as error:
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

    @gen.coroutine
    def get(self):
        """
        GET operation of Web Service
        Returns:
            :return:
        """
        try:
            endpoint_class, matched_groups, pool = EndPointRegister.get_get_service(self.request.uri)
            self._logger.debug(
                "End Point Class: {0} Matched Groups: {1} Pool: {2}".format(endpoint_class, matched_groups, pool))
            if endpoint_class is None:
                self._logger.error("Invalid End Point")
                raise Exceptions.InvalidEndPointException("Invalid End Point")
            self._process_request(matched_groups, endpoint_class, pool)
        except Exceptions.InvalidEndPointException as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()
        except Exceptions as error:
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

    @gen.coroutine
    def put(self):
        """
        PUT operation of Web Service
        Returns:
            :return:
        """
        try:
            endpoint_class, matched_groups, pool = \
                EndPointRegister.get_put_service(self.request.uri)
            self._logger.debug(
                f'End Point Class: {endpoint_class} Matched Groups: {matched_groups} Pool: {pool}')
            if endpoint_class is None:
                self._logger.debug("Invalid End Point")
                raise Exceptions.InvalidEndPointException("Invalid End Point")
            self._process_request(matched_groups, endpoint_class, pool)
        except Exceptions.InvalidEndPointException as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()
        except Exceptions as error:
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        POST operation of Web Service
        Returns:
            :return:
        """
        try:
            endpoint_class, matched_groups, pool = \
                EndPointRegister.get_post_service(self.request.uri)
            self._logger.debug(
                "End Point Class: {0} Matched Groups: {1} Pool: {2}".format(endpoint_class, matched_groups, pool))
            if endpoint_class is None:
                self._logger.debug("Invalid End Point")
                raise Exceptions.InvalidEndPointException("Invalid End Point")
            self._process_request(matched_groups, endpoint_class, pool)
        except Exceptions.InvalidEndPointException as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()
        except Exceptions as error:
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

    @gen.coroutine
    def delete(self, *args, **kwargs):
        """
        DELETE operation of Web Service
        Returns:
            :return:
        """
        try:
            endpoint_class, matched_groups, pool = \
                EndPointRegister.get_delete_service(self.request.uri)
            self._logger.debug(
                "End Point Class: {0} Matched Groups: {1} Pool: {2}".format(endpoint_class, matched_groups, pool))
            if endpoint_class is None:
                self._logger.debug("Invalid End Point")
                raise Exceptions.InvalidEndPointException("Invalid End Point")
            self._process_request(matched_groups, endpoint_class, pool)
        except Exceptions.InvalidEndPointException as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()
        except Exceptions as error:
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

    @tornado.web.asynchronous
    @gen.coroutine
    def _process_request(self, matched_groups, endpoint_class, pool_name):
        """
        Processes Web Service Request and
        writes response code and response description
        Args:
            :param matched_groups:
            :param endpoint_class:
            :param pool_name:
        Returns:
            :return:
        """
        # Opening JSON file
        f = open('webservice/responses/' + endpoint_class + '.json', )
        try:
            request_body = self.request.body
            if self.request.body.decode("utf-8") is not '':
                request_body = tornado.escape.json_decode(self.request.body)

            uri_header = self.request.headers
            uri_header._dict["Remote_ip"] = self.request.remote_ip
            uri_header._as_list["Remote_ip"] = [self.request.remote_ip]

            self._logger.debug("Request URL: {0} Request Header: {1} Request Body: {2}".format(self.request.uri, uri_header, request_body))

            dut_id = None
            try:
                dut_id = matched_groups.get('dut_id')
            except Exception as error:
                self._logger.error("Error: {0} DUT_ID: {1}".format(error, dut_id))

            data = json.load(f)
            response_code = data["response_code"]
            response_body = data["response_body"]

            self.set_status(response_code)
            self.set_header('Content-Type', 'application/json')
            self.write(response_body)
            self.finish()

        except SlotRestartException as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()

        except InvalidPoolException as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(500)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()
        except Exception as error:
            self._logger.error("Error : {}".format(error))
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(str(error))
            self.finish()
        finally:
            # Closing file
            f.close()

    def data_received(self, chunk):
        """
        Data Received method of MAin Handler class.
        Its abstract method of tornado.web.RequestHandler.
        Args:
            :param chunk:
        Returns
            :return:
        """
        pass
