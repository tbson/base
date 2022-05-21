import * as React from "react";
import PageHeading from "components/common/page_heading";
import Table from "./table";
import { messages } from "./config";

export default function Variable() {
    return (
        <>
            <PageHeading>
                <>{messages.heading}</>
            </PageHeading>
            <Table />
        </>
    );
}

Variable.displayName = "Variable";
