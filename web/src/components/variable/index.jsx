import * as React from "react";
import Wrapper from "services/components/wrapper";
import PageHeading from "services/components/page_heading";
import Table from "./table";
import { messages } from "./config";

export default function Variable() {
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

Variable.displayName = "Variable";
