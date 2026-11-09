import java.util.*;
import java.io.*;
public class Solution {

    public static Integer[][][] dp;

    public static int f(int p, int x, int lastTwoDigit, int len, String str) {
        if (p == len) {
            if (lastTwoDigit == 0 || lastTwoDigit == 25 || lastTwoDigit == 50 || lastTwoDigit == 75) {
                return 1;
            }
            return 0;
        }
        if (dp[p][x][lastTwoDigit] != null) {
            return dp[p][x][lastTwoDigit];
        }
        int ans = 0;
        if (str.charAt(p) == 'X') {
            if (x != 10) {
                ans = f(p + 1, x, (lastTwoDigit % 10) * 10 + x, len, str);
            } else {
                for (int i = (p == 0 ? 1 : 0); i < 10; i++) {
                    ans += f(p + 1, i, (lastTwoDigit % 10) * 10 + i, len, str);
                }
            }
        } else if (str.charAt(p) == '_') {
            for (int i = (p == 0 ? 1 : 0); i < 10; i++) {
                ans += f(p + 1, x, (lastTwoDigit % 10) * 10 + i, len, str);
            }
        } else {
            ans += f(p + 1, x, (lastTwoDigit % 10) * 10 + (str.charAt(p) - 48), len, str);
        }
        return dp[p][x][lastTwoDigit] = ans;
    }

    public static void solve(InputReader in, PrintWriter out) {
        String str = in.next();
        int len = str.length();
        if (len == 1) {
            if (str.charAt(0) == '0' || str.charAt(0) == '_' || str.charAt(0) == 'X') {
                out.println(1);
            } else {
                out.println(0);
            }
        } else if (str.charAt(0) == '0') {
            out.println(0);
        } else {
            dp = new Integer[len][11][100];
            out.println(f(0, 10, 0, len, str));
        }
    }

    public static void main(String[] args) {
        InputStream inputStream = System.in;
        OutputStream outputStream = System.out;
        InputReader in = new InputReader(inputStream);
        PrintWriter out = new PrintWriter(outputStream);
        solve(in, out);
        out.close();
    }
    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;

        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 32768);
            tokenizer = null;
        }

        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }

        public int nextInt() {
            return Integer.parseInt(next());
        }

        public long nextLong() {
            return Long.parseLong(next());
        }

    }
}