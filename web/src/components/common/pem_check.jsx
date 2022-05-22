import PemUtils from "services/helpers/pem_utils";

export default function PemCheck({ pem_group, pem, children }) {
    if (PemUtils.hasPermit(pem_group, pem)) {
        return children;
    }
    return null;
}
