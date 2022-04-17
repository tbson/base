import * as React from "react";
import Wrapper from "services/components/wrapper";
import PageHeading from "services/components/page_heading";
import Table from "./table";
import { messages } from "./config";

export default function Role() {
    return (
        <Wrapper>
            <>
                <PageHeading>
                    <>{messages.heading}</>
                </PageHeading>
                <Table />
            </>
        </Wrapper>
    );
}

Role.displayName = "Role";
