import { lazy, useMemo } from "react";

import PageLoader from "../PageLoader";
import { BrowserRouter } from "react-router-dom";
import AppLayout from "../AppLayout";
import type { IRoute } from "../../types/router";
import generateRoutes from "../../utils/routes";

const HomePage = lazy(() => import("../../pages/HomePage"));
const Chat = lazy(() => import("../../pages/Chat"));


const AppRouter = () => {

    const routes: IRoute[] = useMemo(() => [
        {
            path: "/",
            element: <PageLoader><HomePage/></PageLoader>,
            outlet: <AppLayout/>
        },
        {
            path: "/chat",
            element: <Chat/>,
            outlet: <AppLayout/>
        }
    ], [])

    return <BrowserRouter>{generateRoutes(routes, "index-")}</BrowserRouter>;

}

export default AppRouter;