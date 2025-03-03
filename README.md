<h1>P2P Chat with Registration and Bridging</h1>

<p>This repository contains a minimal <strong>peer-to-peer chat</strong> prototype that uses a <strong>central server</strong> for registration and bridging, then lets clients connect <strong>directly</strong> to each other for real-time text chat. It demonstrates key <strong>socket programming</strong> and basic <strong>protocol</strong> concepts, inspired by typical assignments in networking classes.</p>

---

<h2>Overview</h2>

<ul>
    <li><strong>Server</strong> (<code>server.py</code>):
        <ul>
            <li>Maintains a list of connected clients (client ID, IP, port).</li>
            <li>Accepts <code>REGISTER</code>, <code>BRIDGE</code>, and <code>INFO</code> requests from clients.</li>
            <li>Provides bridging info (IP and port) of another client so a direct, peer-to-peer chat can be established.</li>
        </ul>
    </li>
    <li><strong>Client</strong> (<code>client.py</code>):
        <ul>
            <li>Registers itself with the server using <code>/register</code>.</li>
            <li>Requests another client’s IP/port using <code>/bridge</code>.</li>
            <li>Opens a <strong>listening socket</strong> to accept inbound connections.</li>
            <li>Can initiate an <strong>outbound</strong> connection to another client, sending and receiving chat messages directly over TCP.</li>
        </ul>
    </li>
</ul>

---

<h2>Goal</h2>

<ul>
    <li><strong>Educational Objective:</strong></li>
    <ul>
        <li>Practice socket programming in Python.</li>
        <li>Explore how protocols like SIP (Session Initiation Protocol) introduce endpoints for direct communication.</li>
        <li>Understand multi-threaded designs necessary for real-time, two-way data exchange.</li>
    </ul>
</ul>

---

<h2>Instructions</h2>

<h3>1. Setup</h3>
<ul>
    <li>Install <strong>Python 3</strong> on your system.</li>
    <li>Clone this repository or download the <code>server.py</code> and <code>client.py</code> files.</li>
</ul>

<h3>2. Run the Server</h3>
<pre><code>python server.py</code></pre>
<p>The server listens on <code>127.0.0.1:5555</code> by default.</p>

<h3>3. Run a Client</h3>
<pre><code>python client.py &lt;clientID&gt; &lt;listenPort&gt; 127.0.0.1:5555</code></pre>
<p>Example:</p>
<pre><code>python client.py alice 5556 127.0.0.1:5555</code></pre>

<h3>4. Commands</h3>

<table>
    <thead>
        <tr>
            <th>Command</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code>/register</code></td><td>Registers this client with the server.</td></tr>
        <tr><td><code>/info</code></td><td>Requests a list of all known clients.</td></tr>
        <tr><td><code>/bridge</code></td><td>Requests another client's IP/Port for direct connection.</td></tr>
        <tr><td><code>/chat IP:PORT</code></td><td>Connects directly to a peer’s chat socket.</td></tr>
        <tr><td><code>/msg &lt;text&gt;</code></td><td>Sends a text message to the connected peer.</td></tr>
        <tr><td><code>/quit</code></td><td>Closes the client.</td></tr>
    </tbody>
</table>

<h3>5. Running Multiple Clients</h3>
<ul>
    <li>Run another client in a new terminal:</li>
</ul>

<pre><code>python client.py bob 5557 127.0.0.1:5555</code></pre>

---

<h2>Example Usage Flow</h2>
    <strong>On Client A (Alice):</strong> Register with the server.
    <code>/register</code>
    <strong>On Client B (Bob):</strong> Register as well.
    <code>/register</code>

    <strong>On Client A:</strong> Request another client’s info.
    <pre><code>/bridge</code></pre>

    <strong>On Client A:</strong> Connect to Bob.
    <pre><code>/chat 127.0.0.1:5557</code></pre>

    <strong>On Client A:</strong> Send a message.
    <pre><code>/msg Hello Bob!</code></pre>

   <strong>On Client B:</strong> Receives and sees the message.

---

<h2>Quitting</h2>
<ul>
    <li><strong>Client:</strong> Type <code>/quit</code> at the prompt.</li>
    <li><strong>Server:</strong> Press <code>CTRL + C</code> in the terminal.</li>
</ul>

---

<h2>Learning Outcomes</h2>

<ul>
    <li><strong>Socket Programming:</strong> Experience with both <strong>server</strong> and <strong>client</strong> TCP sockets in Python.</li>
    <li><strong>Multi-Threading:</strong> Used separate threads for listening and sending, avoiding Windows console issues.</li>
    <li><strong>Protocol Design:</strong> Implemented custom message headers (<code>REGISTER</code>, <code>BRIDGE</code>, <code>INFO</code>) to establish communication.</li>
    <li><strong>P2P Communication:</strong> Demonstrated how a server can facilitate direct peer-to-peer chat.</li>
</ul>

<p>This project serves as a simple demonstration of how clients can <strong>register</strong> with a central service and then <strong>connect peer-to-peer</strong> using minimal protocol logic.</p>

