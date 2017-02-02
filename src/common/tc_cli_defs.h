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
*	file - tc_cli_defs.h
*	description - shared CLI definitions (cli app and daemon) for TC
*/

#ifndef _TC_CLI_DEFS_H_
#define _TC_CLI_DEFS_H_


/************************************************/
/* includes                                     */
/************************************************/
#include <stdint.h>

/************************************************/
/* Defines                                      */
/************************************************/


/************************************************/
/* Enums                                        */
/************************************************/
enum cli_family_type {
	CLI_FAMILY_COMMON,
	CLI_FAMILY_TC_STAT,
};

enum cli_op_type {
	/* Common types */
	CLI_OP_TYPE_GET_VERSION				  = 0,
	CLI_OP_TYPE_EXIT,				/*  1 */

	/* TC statistics types */
	CLI_OP_TYPE_GET_FILTER				  = 0,
	CLI_OP_TYPE_GET_FAMILY_ACTIONS,			/*  1 */

};


/************************************************/
/* structures                                   */
/************************************************/


/******************************************************************************
 *	Request payload for get tc filter
 *
 */
struct get_tc_filter_cli_req_payload {
	uint32_t         ifindex;
	/* Linux IF index */

	uint32_t         priority;
	/* (-1) means: all priorities for if_index */

	uint32_t         parent;
	/* currently supporting only ingress (TC_INGRESS_PARENT_ID) */

	uint32_t         handdle_id;
	/* (-1) means: all priorities for if_index */
};


#endif /* _TC_CLI_DEFS_H_ */