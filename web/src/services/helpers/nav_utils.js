import Utils from "services/helpers/utils";
import StorageUtils from "services/helpers/storage_utils";
import RequestUtils from "services/helpers/request_utils";

export default class NavUtils {
    /**
     * navigateTo.
     *
     * @param {Navigate} navigate
     */
    static navigateTo(navigate) {
        return (url = "/") => {
            navigate(url);
        };
    }

    /**
     * logout.
     *
     * @param {Navigate} navigate
     */
    static logout(navigate) {
        return () => {
            const baseUrl = RequestUtils.getApiBaseUrl();
            const logoutUrl = `${baseUrl}account/staff/logout/`;
            Utils.toggleGlobalLoading();
            const payload = {
                firebase_token: "",
                staff_id: StorageUtils.getAuthId()
            };
            RequestUtils.apiCall(logoutUrl, payload, "POST")
                .then(() => {
                    NavUtils.cleanAndMoveToLoginPage(navigate);
                })
                .finally(() => {
                    Utils.toggleGlobalLoading(false);
                });
        };
    }

    /**
     * cleanAndMoveToLoginPage.
     *
     * @param {Navigate} navigate
     * @returns {void}
     */
    static cleanAndMoveToLoginPage(navigate) {
        const currentUrl = window.location.href.split("#")[1];
        StorageUtils.removeStorage("auth");
        let loginUrl = "/login";
        if (currentUrl) {
            loginUrl = `${loginUrl}?next=${currentUrl}`;
        }
        if (navigate) {
            Utils.navigateTo(navigate)(loginUrl);
        } else {
            window.location.href = `/#${loginUrl}`;
        }
    }
}
