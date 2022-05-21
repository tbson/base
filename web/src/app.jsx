import { useEffect, useState } from "react";
import { RecoilRoot, useRecoilState } from "recoil";
import { useLocale } from "ttag";
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
import { localeSt } from "src/states";

Utils.responseIntercept();

function Index() {
    const [dataLoaded, setDataLoaded] = useState(false);
    const [locale, setLocale] = useRecoilState(localeSt);
    useLocale(locale);
    useEffect(() => {
        LocaleUtils.fetchLocales().then(() => {
            setDataLoaded(true);
            setLocale(LocaleUtils.setLocale(locale));
        });
    }, []);
    if (!dataLoaded) {
        return <div>Loading...</div>;
    }
    return (
        <div key={locale}>
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
        </div>
    );
}

function App() {
    return (
        <RecoilRoot>
            <Index />
        </RecoilRoot>
    );
}

export default App;
