import StorageUtils from "services/helpers/storage_utils";

export default class PemUtils {
    static hasPermit(pem_group, pem = "view") {
        try {
            const permissions = StorageUtils.getPermissions();
            return permissions[pem_group].includes(pem);
        } catch (_e) {
            return false;
        }
    }
}
