
import { AnimatePresence, motion } from "framer-motion";
import ProfilePicDark from "../../assets/profile-pic-dark.jpeg"
import ProfilePicLight from "../../assets/profile-pic-light.png"
import { useTheme } from "../../context/ThemeContext";

const Avatar = () => {

    const {theme} = useTheme();
  const src = theme === "light" ? ProfilePicLight : ProfilePicDark;

    return (
    <div className="relative h-10 w-10">
      <AnimatePresence mode="wait">
        <motion.img
          key={src} // important for AnimatePresence to trigger exit/enter
          src={src}
          alt="Profile"
          className="absolute inset-0 h-full w-full rounded-full object-cover border border-zinc-200 dark:border-zinc-800 cursor-pointer"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
          whileHover={{
            scale: 1.1,
            boxShadow: "0px 4px 15px rgba(0,0,0,0.2)",
          }}
          whileTap={{ scale: 0.98 }}
        />
      </AnimatePresence>
    </div>
  );
}

export default Avatar;