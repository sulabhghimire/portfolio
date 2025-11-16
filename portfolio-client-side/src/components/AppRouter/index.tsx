import { lazy, useMemo } from "react";

import PageLoader from "../PageLoader";
import { BrowserRouter } from "react-router-dom";
import AppLayout from "../AppLayout";
import type { IRoute } from "../../types/router";
import generateRoutes from "../../utils/routes";

const HomePage = lazy(() => import("../../pages/HomePage"));

const AppRouter = () => {

    const routes: IRoute[] = useMemo(() => [
        {
            path: "/",
            index: true,
            element: <PageLoader><HomePage/></PageLoader>,
            outlet: <AppLayout/>
        }
    ], [])

    return <BrowserRouter>{generateRoutes({routes, routerPrefix:"main"})}</BrowserRouter>;

}

export default AppRouter;