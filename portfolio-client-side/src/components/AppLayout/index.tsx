import { Outlet } from "react-router-dom";
import DefaultHeader from "../DefaultHeader";
import DefaultFooter from "../DefaultFooter";
import { motion } from "framer-motion";


type ComponentOrNull = React.FC<any> | null;

interface IAppLayoutProps {
    Header?: ComponentOrNull;
    Footer?: ComponentOrNull;
}

const AppLayout = ({ Header, Footer }: IAppLayoutProps) => {

    const HeaderComponent = Header || DefaultHeader;
    const FooterComponent = Footer || DefaultFooter;

    return (
        <div className="flex flex-col h-screen bg-white dark:bg-zinc-950">
            <div className="sticky top-0 z-40">
                <HeaderComponent />
            </div>

            <motion.main
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.35 }}
                className="flex-1 overflow-auto"
            >
                <Outlet />
            </motion.main>

            <FooterComponent />
        </div>
    )


}

export default AppLayout;