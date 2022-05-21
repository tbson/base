import * as React from "react";
import DatePicker from "services/components/DatePicker";
import Utils from "services/helpers/utils";

/**
 * DateInput.
 *
 * @param {Object} props
 * @param {string} props.value
 * @param {function} props.onChange
 * @param {string} props.label
 * @returns {ReactElement}
 */
export default function DateInput({ value, onChange }) {
    return (
        <DatePicker
            value={value}
            onChange={onChange}
            format={Utils.DATE_REABLE_FORMAT}
            style={{ width: "100%" }}
        />
    );
}
