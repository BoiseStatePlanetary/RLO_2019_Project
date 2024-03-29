! ***********************************************************************
!
!   Copyright (C) 2012  Bill Paxton
!
!   this file is part of mesa.
!
!   mesa is free software; you can redistribute it and/or modify
!   it under the terms of the gnu general library public license as published
!   by the free software foundation; either version 2 of the license, or
!   (at your option) any later version.
!
!   mesa is distributed in the hope that it will be useful, 
!   but without any warranty; without even the implied warranty of
!   merchantability or fitness for a particular purpose.  see the
!   gnu library general public license for more details.
!
!   you should have received a copy of the gnu library general public license
!   along with this software; if not, write to the free software
!   foundation, inc., 59 temple place, suite 330, boston, ma 02111-1307 usa
!
! ***********************************************************************
 
      module run_star_extras 

      use star_lib
      use star_def
      use const_def
      use const_def
      use chem_def
      use binary_def
      
      implicit none
      
      integer :: time0, time1, clock_rate
      real(dp), parameter :: expected_runtime = 1 ! minutes

      integer, parameter :: restart_info_alloc = 1
      integer, parameter :: restart_info_get = 2
      integer, parameter :: restart_info_put = 3
      
      
      contains
      
      subroutine extras_controls(s, ierr)
         type (star_info), pointer :: s
         integer, intent(out) :: ierr
         ierr = 0
      end subroutine extras_controls
      
      
      integer function extras_startup(s, id, restart, ierr)
         type (star_info), pointer :: s
         integer, intent(in) :: id
         logical, intent(in) :: restart
         integer, intent(out) :: ierr
         integer :: restart_time, prev_time_used
         ierr = 0
         if (.not. restart) then
            call system_clock(time0,clock_rate)
            call alloc_restart_info(s)
         else
            call unpack_restart_info(s)
            call system_clock(restart_time,clock_rate)
            prev_time_used = time1 - time0
            time1 = restart_time
            time0 = time1 - prev_time_used
         end if
         extras_startup = keep_going
      end function extras_startup
      

      integer function extras_check_model(s, id, id_extra)
         implicit none
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra
         type (binary_info), pointer :: b
	 integer :: ierr

         extras_check_model = keep_going

         call binary_ptr(b,ierr)
         ierr = 0

	! PA: start code for irradiation
	!if (s% id == 1) then
        !    s% column_depth_for_irradiation = 100.0
        !    s% irradiation_flux = s2%L(1) / (4.0*pi*b%separation**2)
	!endif
	b%s1%column_depth_for_irradiation = b%s1%x_ctrl(1)
	b%s1%irradiation_flux = b%s2%L(1) / (4.0*pi*b%separation**2)
        b%s2%column_depth_for_irradiation = b%s2%x_ctrl(1)
        b%s2%irradiation_flux = b%s1%L(1) / (4.0*pi*b%separation**2)
	! PA: end code for irradiation

	! PA: set companion radius for orbital decay
	b% R_companion =  b%s2%r(1)/Rsun
	! PA: end code for companion radius

	! PA
	!print *,"b% mdot_thin,b% mtransfer_rate=",b%mdot_thin,b% mtransfer_rate
	!print *,"b% s_donor% mstar_dot=",b% s_donor% mstar_dot
	!print *,"b% s_accretor% mstar_dot=",b% s_accretor% mstar_dot
	! PA

      end function extras_check_model


      integer function how_many_extra_history_columns(s, id, id_extra)
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra
         how_many_extra_history_columns = 1
      end function how_many_extra_history_columns
      
      
      subroutine data_for_extra_history_columns(s, id, id_extra, n, names, vals, ierr)
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra, n
         character (len=maxlen_profile_column_name) :: names(n)
         real(dp) :: vals(n)
         integer, intent(out) :: ierr
         real(dp) :: dt
         ierr = 0
         if (n /= 1) then
            stop 'bad n for data_for_extra_history_columns'
         end if
         dt = dble(time1 - time0) / clock_rate / 60
         names(1) = 'runtime_minutes'
         vals(1) = dt
      end subroutine data_for_extra_history_columns

      
      integer function how_many_extra_profile_columns(s, id, id_extra)
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra
         how_many_extra_profile_columns = 0
      end function how_many_extra_profile_columns
      
      
      subroutine data_for_extra_profile_columns(s, id, id_extra, n, nz, names, vals, ierr)
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra, n, nz
         character (len=maxlen_profile_column_name) :: names(n)
         real(dp) :: vals(nz,n)
         integer, intent(out) :: ierr
         integer :: k
         ierr = 0
      end subroutine data_for_extra_profile_columns
      

      integer function extras_finish_step(s, id, id_extra)
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra
         extras_finish_step = keep_going
         call system_clock(time1,clock_rate)
         call store_restart_info(s)
      end function extras_finish_step
      
      
      subroutine extras_after_evolve(s, id, id_extra, ierr)
         type (star_info), pointer :: s
         integer, intent(in) :: id, id_extra
         integer, intent(out) :: ierr
         real(dp) :: dt
         ierr = 0
         dt = dble(time1 - time0) / clock_rate / 60
         if (dt > 10*expected_runtime) then
            write(*,'(/,a30,2f18.6,a,/)') '>>>>>>> EXCESSIVE runtime', &
               dt, expected_runtime, '   <<<<<<<<<  ERROR'
         else
            write(*,'(/,a50,2f18.6,99i10/)') 'runtime, retries, backups, steps', &
               dt, expected_runtime, s% num_retries, s% num_backups, s% model_number
         end if
      end subroutine extras_after_evolve
      
      
      ! routines for saving and restoring data so can do restarts

      
      subroutine alloc_restart_info(s)
         type (star_info), pointer :: s
         call move_restart_info(s,restart_info_alloc)
      end subroutine alloc_restart_info
      
      
      subroutine unpack_restart_info(s)
         type (star_info), pointer :: s
         call move_restart_info(s,restart_info_get)
      end subroutine unpack_restart_info
      
      
      subroutine store_restart_info(s)
         type (star_info), pointer :: s
         call move_restart_info(s,restart_info_put)
      end subroutine store_restart_info
      
      
      subroutine move_restart_info(s,op)
         type (star_info), pointer :: s
         integer, intent(in) :: op
         
         integer :: i, j, num_ints, num_dbls, ierr
         
         i = 0
         ! call move_int or move_flg 
         call move_int(time0)
         call move_int(time1)
         
         num_ints = i
         
         i = 0
         ! call move_dbl 
         
         num_dbls = i
         
         if (op /= restart_info_alloc) return
         if (num_ints == 0 .and. num_dbls == 0) return
         
         ierr = 0
         call star_alloc_extras(s% id, num_ints, num_dbls, ierr)
         if (ierr /= 0) then
            write(*,*) 'failed in star_alloc_extras'
            write(*,*) 'alloc_extras num_ints', num_ints
            write(*,*) 'alloc_extras num_dbls', num_dbls
            stop 1
         end if
         
         contains
         
         subroutine move_dbl(dbl)
            real(dp) :: dbl
            i = i+1
            select case (op)
            case (restart_info_get)
               dbl = s% extra_work(i)
            case (restart_info_put)
               s% extra_work(i) = dbl
            end select
         end subroutine move_dbl
         
         subroutine move_int(int)
            integer :: int
            include 'formats'
            i = i+1
            select case (op)
            case (restart_info_get)
               !write(*,3) 'restore int', i, s% extra_iwork(i)
               int = s% extra_iwork(i)
            case (restart_info_put)
               !write(*,3) 'save int', i, int
               s% extra_iwork(i) = int
            end select
         end subroutine move_int
         
         subroutine move_flg(flg)
            logical :: flg
            i = i+1
            select case (op)
            case (restart_info_get)
               flg = (s% extra_iwork(i) /= 0)
            case (restart_info_put)
               if (flg) then
                  s% extra_iwork(i) = 1
               else
                  s% extra_iwork(i) = 0
               end if
            end select
         end subroutine move_flg

      end subroutine move_restart_info
      
      


      end module run_star_extras
      
