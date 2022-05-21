import * as React from "react";
import { useState, useEffect } from "react";
import Utils from "services/helpers/utils";
import Waiting from "components/common/waiting";

export default function Component() {
    const [spinning, setSpinning] = useState(false);

    const eventHandler = ({ detail: spinning }) => setSpinning(spinning);

    useEffect(() => {
        Utils.event.listen("TOGGLE_SPINNER", eventHandler);
        return () => {
            Utils.event.remove("TOGGLE_SPINNER", eventHandler);
        };
    }, []);

    return spinning ? <Waiting /> : null;
}
