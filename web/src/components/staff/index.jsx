import * as React from "react";
import SideBarLayout from "components/common/layout/side_bar";
import PageHeading from "components/common/page_heading";
import Table from "./table";
import { messages } from "./config";

export default function Staff() {
    return (
        <SideBarLayout>
            <>
                <PageHeading>
                    <>{messages.heading}</>
                </PageHeading>
                <Table />
            </>
        </SideBarLayout>
    );
}

Staff.displayName = "Staff";
