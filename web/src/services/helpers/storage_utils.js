import { LOCAL_STORAGE_PREFIX } from "src/consts";
import Utils from "services/helpers/utils";

export default class StorageUtils {
    /**
     * setStorage.
     *
     * @param {string} key
     * @param {string | Dict} value
     * @returns {void}
     */
    static setStorage(key, value) {
        try {
            localStorage.setItem(
                LOCAL_STORAGE_PREFIX + "_" + key,
                JSON.stringify(value)
            );
        } catch (error) {
            console.log(error);
        }
    }

    /**
     * setStorageObj.
     *
     * @param {Object} input
     * @returns {void}
     */
    static setStorageObj(input) {
        for (const key in input) {
            const value = input[key];
            this.setStorage(key, value);
        }
    }

    /**
     * getStorageObj.
     *
     * @param {string} key
     * @returns {Object}
     */
    static getStorageObj(key) {
        try {
            const value = StorageUtils.parseJson(
                localStorage.getItem(LOCAL_STORAGE_PREFIX + "_" + key)
            );
            if (value && typeof value === "object") {
                return value;
            }
            return {};
        } catch (error) {
            console.log(error);
            return {};
        }
    }

    /**
     * getStorageStr.
     *
     * @param {string} key
     * @returns {string}
     */
    static getStorageStr(key) {
        try {
            const value = StorageUtils.parseJson(
                localStorage.getItem(LOCAL_STORAGE_PREFIX + "_" + key)
            );
            if (!value || typeof value === "object") {
                return "";
            }
            return String(value);
        } catch (error) {
            return "";
        }
    }

    /**
     * getToken.
     *
     * @returns {string}
     */
    static getToken() {
        const authObj = this.getStorageObj("auth");
        const token = authObj.token;
        return token ? token : "";
    }

    /**
     * getAuthId.
     *
     * @returns {number}
     */
    static getAuthId() {
        const authObj = this.getStorageObj("auth");
        return authObj.id;
    }

    /**
     * removeStorage.
     *
     * @param {string} key
     * @returns {void}
     */
    static removeStorage(key) {
        localStorage.removeItem(LOCAL_STORAGE_PREFIX + "_" + key);
    }

    /**
     * parseJson.
     *
     * @param {string} input
     * @returns {string}
     */
    static parseJson(input) {
        try {
            return JSON.parse(input);
        } catch (error) {
            return String(input);
        }
    }

    /**
     * getVisibleMenus.
     *
     * @returns {string[]}
     */
    static getVisibleMenus() {
        const authObj = StorageUtils.getStorageObj("auth");
        const menu = authObj.visible_menus;
        return menu ? menu : [];
    }
}
