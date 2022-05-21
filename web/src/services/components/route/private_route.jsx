import * as React from "react";
import { Outlet, Navigate } from "react-router-dom";
import StorageUtils from "services/helpers/storage_utils";

export default function PrivateRoute() {
    return StorageUtils.getToken() ? <Outlet /> : <Navigate to="/login" />;
}

PrivateRoute.displayName = "PrivateRoute";
