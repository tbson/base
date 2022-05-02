import StorageUtils from "services/helpers/storage_utils";
import StaffProfile from "components/staff/profile";
export default function Profile() {
    const userType = StorageUtils.getUserType();
    if (userType === "staff") {
        return <StaffProfile />;
    }
    return null;
}

Profile.displayName = "Profile";
