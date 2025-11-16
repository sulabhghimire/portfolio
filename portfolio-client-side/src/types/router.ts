import type { JSX } from "react";

export interface IRoute {
    path: string;
    element: JSX.Element;
    outlet?: JSX.Element;
    outletKey?: string;
    index?: boolean
}
