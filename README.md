<article class="markdown-body entry-content" itemprop="text"><h1><a id="user-content-atc---accelerated-tc" class="anchor" href="#atc---accelerated-tc" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>ATC - accelerated TC</b></h1>

<hr>

<h3><a id="user-content-overview" class="anchor" href="#overview" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>Overview</b></h3>

<hr>

<pre><code>
The Linux® Traffic Control (TC) is a network
ingress and egress classification, action and traffic management subsystem. It
was first developed for the purpose of classifying packets and for traffic
management and virtual output queuing but has since evolved to support
arbitrary actions not related specifically to traffic management. 

The Mellanox Accelerated TC (ATC) solution improves upon the Linux TC by
moving the packet processing functionality from Linux network stack to the Indigo
NPS-400 network processor, installed in the Indigo NPS-400 Platform to improve
performance to up to 400Gb/s.

</code></pre>

<h3><a id="user-content-prepare-atc-enviroment" class="anchor" href="#prepare-atc-enviroment" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>Prepare ATC enviroment</b></h3>

<hr>

<p><b>1. Pull latest ATC from GitHub</b></p>

<pre><code>git clone git@github.com:Mellanox/ATC.git
git checkout release/24.0100
</code></pre>

<p><b>2. Download openNPU</b></p>

<p><a href="http://opennpu.org/how-to-download/">openNPU</a></p>

<pre><code>
  Follow instructions in the above link on how to setup EZdk openNPU enviroment.

  The version must be 18_0400.
</code></pre>

<h4><a id="user-content-3-remove-ezdk-soft-link" class="anchor" href="#3-remove-ezdk-soft-link" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>3. Remove EZdk soft link</b></h4>

<pre><code>  Go to ATC project folder and remove the soft link to EZdk. use the following commands:
  rm EZdk
</code></pre>

<h4><a id="user-content-4-add-soft-link-to-opennpu-ezdk" class="anchor" href="#4-add-soft-link-to-opennpu-ezdk" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>4. Add soft link to openNPU EZdk</b></h4>

<pre><code>Use the following command to link EZdk openNPU to ATC application:
ln -s &lt;local openNPU folder&gt;/EZdk EZdk
</code></pre>

<h3><a id="user-content-build-atc-application" class="anchor" href="#build-atc-application" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>Build ATC application</b></h3>

<hr>

<p>The ATC build process has 2 steps:</p>

<ul>
<li><p>Build ATC application</p></li>
<li><p>Build ATC debian package</p></li>
</ul>

<h4><a id="user-content-compile-atc" class="anchor" href="#compile-atc" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>Compile ATC</b></h4>

<h1></h1>

<pre><code>To compile the ATC application go to ALVS directory and run make atc command.
Make will compile the control plane (cp.mk) code and the data plane (dp.mk) code.
</code></pre>

<h4><a id="user-content-build-atc-debian-package" class="anchor" href="#build-atc-debian-package" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a><b>Build ATC debian package</b></h4>

<h1></h1>

<p>In order to build a debian package you must run the following command on a debian machine:</p>

<pre><code>       make deb-atc
</code></pre>

<p>In case you don't have a debian machine, use a virtual machine running debian and mount</p>

<p>the ATC directory on it. Afterwards, perform the above command in the debian machine.</p>

<p>The output of the above command is a debian package file under ALVS folder. for example: </p>

<pre><code>      atc_24.0100.0000_amd64.deb
</code></pre>

<p>Copy the package to the NPS-400 appliance box and install it using the following command:</p>

<pre><code>      dpkg -i atc_24.0100.0000_amd64.deb - also works for upgrade.
</code></pre>

<p>In case you want to remove ATC package from NPS-400 appliance, run the following command:</p>

<pre><code>      dpkg -r atc
</code></pre>

<p>To purge (also removes ATC config):</p>

<pre><code>      dpkg -P atc
</code></pre>

<p>For more information on ATC application, features, setup and more see:</p>

<ul>
<li><p>Manual [add link here]</p></li>
<li><p>Release notes [add link here]</p></li>
</ul>
