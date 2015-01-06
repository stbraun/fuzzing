import System.IO
import System.Environment
import Control.Monad
import System.Exit
import System.Random

main :: IO ()
main = do
  args <- getArgs
  when ("-c" `elem` args) $ do
    exitWith (ExitFailure 1)
  when ("-p" `elem` args) $ do
    exit <- shallFail
    when (exit) $ do
      exitWith (ExitFailure 2)
  input <- getLine -- just wait until test kills this process.
  putStrLn input
  exitWith ExitSuccess


shallFail :: IO Bool
shallFail = do
  rnd <- getStdRandom (randomR (1, 6))
  return ((rnd :: Integer) > (1 :: Integer))
