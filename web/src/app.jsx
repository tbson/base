import { useEffect, useState } from "react";
import { RecoilRoot } from "recoil";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import PrivateRoute from "services/components/route/private_route.jsx";
import NotMatch from "services/components/route/not_match";
import ScrollToTop from "services/components/scroll_to_top";
import Utils from "services/helpers/utils";
import LocaleUtils from "services/helpers/locale_utils";
import Spinner from "services/components/spinner";
import Login from "components/auth/login";
import Profile from "components/auth/profile";
import Staff from "components/staff";
import Role from "components/role";
import Variable from "components/variable";

Utils.responseIntercept();

function App() {
    const [dataLoaded, setDataLoaded] = useState(false);
    useEffect(() => {
        LocaleUtils.fetchLocales().then(() => {
            LocaleUtils.activateLocale();
            setDataLoaded(true);
        });
    }, []);
    if (!dataLoaded) {
        return <div>Loading...</div>;
    }
    return (
        <RecoilRoot>
            <Spinner />
            <BrowserRouter>
                <ScrollToTop />
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/" element={<PrivateRoute />}>
                        <Route path="/" element={<Profile />} />
                        <Route path="/staff" element={<Staff />} />
                        <Route path="/role" element={<Role />} />
                        <Route path="/variable" element={<Variable />} />
                    </Route>
                    <Route path="*" element={<NotMatch />} />
                </Routes>
            </BrowserRouter>
        </RecoilRoot>
    );
}

export default App;
