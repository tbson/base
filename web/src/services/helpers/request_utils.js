import axios from "axios";
import Utils from "services/helpers/utils";
import NavUtils from "services/helpers/nav_utils";
import StorageUtils from "services/helpers/storage_utils";
import { PROTOCOL, DOMAIN, API_PREFIX } from "src/consts";

export default class RequestUtils {
    /**
     * Prepare JSON payload for HTTP request
     * @param {Object} data
     * @returns {Object}
     */
    static getJsonPayload(data) {
        return {
            data: data,
            "Content-Type": "application/json"
        };
    }

    /**
     * Prepare FormData payload for HTTP request
     * @param {Object} data
     * @returns {Object}
     */
    static getFormDataPayload(data) {
        const formData = new FormData();
        for (const key in data) {
            const value = data[key];
            formData.set(key, value);
        }
        return {
            data: formData,
            "Content-Type": ""
        };
    }

    /**
     * Check if any key of a map contains file
     * @param {Object} data
     * @returns {boolean}
     */
    static fileInObject(data) {
        return !!Object.values(data).filter((item) => item instanceof Blob).length;
    }

    /**
     * Prepare payload for axios, if method is not POST or PUT
     *  Append it to a map with params key
     * @param {string} method
     * @param {Object} data
     * @returns {Object}
     */
    static convertParams(method, data) {
        if (["post", "put"].includes(method.toLowerCase())) return data;
        return { params: data };
    }

    /**
     * Make a HTTP request using Axios, do not check for refreshing token
     * @param {string} url
     * @param {Object} params
     * @param {string} method - method: get, post, put, delete
     * @returns {Promise} Axios response promise
     */
    static async request(url, params = {}, method = "get", blobResponseType = false) {
        const { data, "Content-Type": contentType } = RequestUtils.fileInObject(params)
            ? RequestUtils.getFormDataPayload(params)
            : RequestUtils.getJsonPayload(params);
        const token = StorageUtils.getToken();
        const config = {
            method,
            baseURL: RequestUtils.getApiBaseUrl(),
            url,
            headers: {
                Authorization: token ? `JWT ${token}` : undefined,
                "Content-Type": contentType
            }
        };
        if (blobResponseType) {
            config.responseType = "blob";
        }
        if (!Utils.isEmpty(params) && method === "get") {
            const query = new URLSearchParams(params).toString();
            config.url = [config.url, query].join("?");
        } else {
            config.data = RequestUtils.convertParams(method, data);
        }
        return await axios(config);
    }

    /**
     * Make a HTTP request using Axios, checking for refreshing token also
     * @param {string} url
     * @param {Object} params
     * @param {string} method - method: get, post, put, delete
     * @returns {Promise} Axios response promise
     */
    static async apiCall(url, params = {}, method = "get", blobResponseType = false) {
        const emptyError = {
            response: {
                data: {}
            }
        };
        try {
            return await RequestUtils.request(url, params, method, blobResponseType);
        } catch (err) {
            if (err.response.status === 401) {
                const refreshUrl = "account/user/refresh-token/";
                const checkUrl = "account/user/refresh-check/";
                try {
                    const refreshTokenResponse = await RequestUtils.request(
                        refreshUrl,
                        { refresh_token: StorageUtils.getRefreshToken() },
                        "POST"
                    );
                    const token = refreshTokenResponse.data.token;
                    StorageUtils.setToken(token);

                    try {
                        return await RequestUtils.request(url, params, method);
                    } catch (err) {
                        if (err.response.status === 401) {
                            // Logout
                            NavUtils.cleanAndMoveToLoginPage();
                            return Promise.reject(emptyError);
                        }
                        // Return error
                        return Promise.reject(err);
                    }
                } catch (err) {
                    console.log(err);
                    RequestUtils.request(checkUrl).catch(() => {
                        // Logout
                        NavUtils.cleanAndMoveToLoginPage();
                        return Promise.reject(emptyError);
                    });
                }
            }
            // Return error
            return Promise.reject(err);
        }
    }

    /**
     * setFormErrors.
     *
     * @param {Dict} errors
     * @returns {FormikErrorDict}
     */
    static setFormErrors(errors) {
        return Object.entries(errors)
            .map(([key, value]) => [key, Utils.errorFormat(value)])
            .filter((item) => !!item[1].length)
            .reduce((result, [key, value]) => {
                result[key] = value;
                return result;
            }, {});
    }

    /**
     * errorFormat.
     *
     * @param {string | number | Dict | string[]} input
     * @returns {string[]}
     */
    static errorFormat(input) {
        if (!input) return [];
        if (typeof input === "string") return [input];
        if (Array.isArray(input))
            return input.filter((item) => item).map((item) => item.toString());
        return [];
    }

    /**
     * getApiBaseUrl.
     *
     * @returns {string}
     */
    static getApiBaseUrl() {
        return PROTOCOL + DOMAIN + API_PREFIX;
    }

    /**
     * prefixMapValues.
     *
     * @param {Object} input
     * @param {string} input.prefix
     * @param {Object} input.endpoints
     * @returns {Object}
     */
    static prefixMapValues({ prefix, endpoints }) {
        const result = {};
        for (const key in endpoints) {
            const value = endpoints[key];
            result[key] = [prefix, value].join("/");
            if (result[key][result[key].length - 1] !== "/") {
                result[key] += "/";
            }
        }
        return result;
    }

    /**
     * handleDownload.
     *
     * @param {Object} data
     * @param {string} filename
     * @returns {Object}
     */
    static handleDownload(data, filename) {
        const url = window.URL.createObjectURL(new Blob([data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
    }
}
