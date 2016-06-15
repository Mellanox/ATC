/* Copyright (c) 2016 Mellanox Technologies, Ltd. All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*
* 1. Redistributions of source code must retain the above copyright
*    notice, this list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright
*    notice, this list of conditions and the following disclaimer in the
*    documentation and/or other materials provided with the distribution.
* 3. Neither the names of the copyright holders nor the names of its
*    contributors may be used to endorse or promote products derived from
*    this software without specific prior written permission.
*
* Alternatively, this software may be distributed under the terms of the
* GNU General Public License ("GPL") version 2 as published by the Free
* Software Foundation.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.
*
*  Project:             NPS400 ALVS application
*  File:                alvs_packet_processing.c
*  Desc:                classification functionality for ALVS
*/

#include "alvs_packet_processing.h"

/******************************************************************************
 * \brief       alvs packet processing function
 *              perform connection classification - 5 tuple - DIP, dest port, CIP, client port and IP protocol
 *
 * \return        void
 */
void alvs_packet_processing(uint8_t *frame_base, struct iphdr *ip_hdr)
{
	 uint32_t rc;
	 uint32_t found_result_size;
	 struct  alvs_conn_classification_result *conn_class_res_ptr;
	 struct tcphdr *tcp_hdr = (struct tcphdr *)((uint8_t *)ip_hdr + (ip_hdr->ihl << 2));

	 cmem_alvs.conn_class_key.virtual_ip = ip_hdr->daddr;
	 cmem_alvs.conn_class_key.virtual_port = tcp_hdr->dest;
	 cmem_alvs.conn_class_key.client_ip = ip_hdr->saddr;
	 cmem_alvs.conn_class_key.client_port = tcp_hdr->source;
	 cmem_alvs.conn_class_key.protocol = ip_hdr->protocol;

	 alvs_write_log(LOG_DEBUG, "Connection (0x%x:%d --> 0x%c:%d, protocol=%d)...",
			cmem_alvs.conn_class_key.client_ip,
			cmem_alvs.conn_class_key.client_port,
			cmem_alvs.conn_class_key.virtual_ip,
			cmem_alvs.conn_class_key.virtual_port,
			cmem_alvs.conn_class_key.protocol);

	 rc = ezdp_lookup_hash_entry(&shared_cmem_alvs.conn_class_struct_desc,
				     (void *)&cmem_alvs.conn_class_key,
				     sizeof(struct alvs_conn_classification_key),
				     (void **)&conn_class_res_ptr,
				     &found_result_size, 0,
				     cmem_wa.alvs_wa.conn_hash_wa,
				     sizeof(cmem_wa.alvs_wa.conn_hash_wa));

	if (rc == 0) {
		alvs_write_log(LOG_DEBUG, "Connection exists (fast path)");
		alvs_conn_data_path(frame_base, ip_hdr, tcp_hdr, conn_class_res_ptr->conn_index);
	} else {
		/*handle slow path  - opening new connection*/
		alvs_write_log(LOG_DEBUG, "New connection (slow path)");
		alvs_unknown_packet_processing(frame_base, ip_hdr, tcp_hdr);
	}
}