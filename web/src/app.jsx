import * as React from "react";
import { useEffect, useState } from "react";
import { RecoilRoot, useRecoilState } from "recoil";
import { useLocale } from "ttag";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import { localeSt } from "src/states";
import PrivateRoute from "services/components/route/private_route.jsx";
import NotMatch from "services/components/route/not_match";
import ScrollToTop from "services/components/scroll_to_top";
import Utils from "services/helpers/utils";
import LocaleUtils from "services/helpers/locale_utils";
import Spinner from "services/components/spinner";

const Login = React.lazy(() => import("components/auth/login"));
const Profile = React.lazy(() => import("components/auth/profile"));
const Staff = React.lazy(() => import("components/staff"));
const Role = React.lazy(() => import("components/role"));
const Variable = React.lazy(() => import("components/variable"));

Utils.responseIntercept();

function FallBack() {
    return <div>Loading...</div>;
}

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
                    <Route
                        path="/login"
                        element={
                            <React.Suspense fallback={<FallBack />}>
                                <Login />
                            </React.Suspense>
                        }
                    />
                    <Route path="/" element={<PrivateRoute />}>
                        <Route
                            path="/"
                            element={
                                <React.Suspense fallback={<FallBack />}>
                                    <Profile />
                                </React.Suspense>
                            }
                        />
                        <Route
                            path="/staff"
                            element={
                                <React.Suspense fallback={<FallBack />}>
                                    <Staff />
                                </React.Suspense>
                            }
                        />
                        <Route
                            path="/role"
                            element={
                                <React.Suspense fallback={<FallBack />}>
                                    <Role />
                                </React.Suspense>
                            }
                        />
                        <Route
                            path="/variable"
                            element={
                                <React.Suspense fallback={<FallBack />}>
                                    <Variable />
                                </React.Suspense>
                            }
                        />
                    </Route>
                    <Route
                        path="*"
                        element={
                            <React.Suspense fallback={<FallBack />}>
                                <NotMatch />
                            </React.Suspense>
                        }
                    />
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
